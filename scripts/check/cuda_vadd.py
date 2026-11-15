"""컴파일러 없이 CUDA 연산 확인: 드라이버 API(libcuda) + PTX JIT로 벡터 덧셈."""
import array
import ctypes as C
import sys

PTX = r"""
.version 7.0
.target sm_50
.address_size 64
.visible .entry vadd(.param .u64 pa, .param .u64 pb, .param .u64 pc, .param .u32 n)
{
  .reg .pred p; .reg .b32 r<5>; .reg .b64 rd<10>; .reg .f32 f<4>;
  ld.param.u64 rd1, [pa]; ld.param.u64 rd2, [pb]; ld.param.u64 rd3, [pc]; ld.param.u32 r1, [n];
  mov.u32 r2, %ctaid.x; mov.u32 r3, %ntid.x; mov.u32 r4, %tid.x;
  mad.lo.s32 r2, r2, r3, r4;
  setp.ge.u32 p, r2, r1;
  @p bra DONE;
  cvta.to.global.u64 rd4, rd1; cvta.to.global.u64 rd5, rd2; cvta.to.global.u64 rd6, rd3;
  mul.wide.u32 rd7, r2, 4;
  add.s64 rd8, rd4, rd7; ld.global.f32 f1, [rd8];
  add.s64 rd8, rd5, rd7; ld.global.f32 f2, [rd8];
  add.f32 f3, f1, f2;
  add.s64 rd9, rd6, rd7; st.global.f32 [rd9], f3;
DONE:
  ret;
}
"""

cu = C.CDLL("libcuda.so.1")

def ck(ret, what):
    if ret != 0:
        msg = C.c_char_p()
        cu.cuGetErrorString(ret, C.byref(msg))
        sys.exit(f"{what} 실패: {ret} {msg.value.decode() if msg.value else ''}")

ck(cu.cuInit(0), "cuInit")
drv = C.c_int(); cu.cuDriverGetVersion(C.byref(drv))
dev = C.c_int(); ck(cu.cuDeviceGet(C.byref(dev), 0), "cuDeviceGet")
name = C.create_string_buffer(128); cu.cuDeviceGetName(name, 128, dev)
major, minor = C.c_int(), C.c_int()
cu.cuDeviceGetAttribute(C.byref(major), 75, dev)   # COMPUTE_CAPABILITY_MAJOR
cu.cuDeviceGetAttribute(C.byref(minor), 76, dev)   # COMPUTE_CAPABILITY_MINOR
print(f"device {name.value.decode()}, CC {major.value}.{minor.value}, driver API {drv.value}")

ctx = C.c_void_p()
ck(cu.cuDevicePrimaryCtxRetain(C.byref(ctx), dev), "cuDevicePrimaryCtxRetain")
ck(cu.cuCtxSetCurrent(ctx), "cuCtxSetCurrent")
mod, fn = C.c_void_p(), C.c_void_p()
ck(cu.cuModuleLoadData(C.byref(mod), PTX.encode()), "cuModuleLoadData (PTX JIT)")
ck(cu.cuModuleGetFunction(C.byref(fn), mod, b"vadd"), "cuModuleGetFunction")

N = 1 << 20
nbytes = C.c_size_t(4 * N)
a = array.array("f", (float(i) for i in range(N)))
b = array.array("f", [2.0]) * N
c = array.array("f", bytes(4 * N))

d = [C.c_uint64() for _ in range(3)]
for x in d:
    ck(cu.cuMemAlloc_v2(C.byref(x), nbytes), "cuMemAlloc")
ck(cu.cuMemcpyHtoD_v2(d[0], C.c_void_p(a.buffer_info()[0]), nbytes), "HtoD a")
ck(cu.cuMemcpyHtoD_v2(d[1], C.c_void_p(b.buffer_info()[0]), nbytes), "HtoD b")

n = C.c_uint32(N)
params = (C.c_void_p * 4)(*[C.addressof(x) for x in (d[0], d[1], d[2], n)])
ck(cu.cuLaunchKernel(fn, (N + 255) // 256, 1, 1, 256, 1, 1, 0, None, params, None), "cuLaunchKernel")
ck(cu.cuCtxSynchronize(), "cuCtxSynchronize")
ck(cu.cuMemcpyDtoH_v2(C.c_void_p(c.buffer_info()[0]), d[2], nbytes), "DtoH c")
for x in d:
    cu.cuMemFree_v2(x)

bad = sum(1 for i in range(N) if c[i] != a[i] + 2.0)
print(f"vadd N={N}: mismatches={bad} -> {'OK' if bad == 0 else 'FAIL'}")
if bad:
    sys.exit(1)

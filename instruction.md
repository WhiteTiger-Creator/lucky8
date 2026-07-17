The telemetry codec at `/app/codec.py` stopped interoperating with the sensor bus after the firmware was updated, and frames it produces are now rejected by conforming devices. Bring it back into spec.

`/app/docs/frame_spec.md` is the authoritative VTF-1 wire format. Fix `/app/codec.py` so its `encode(payload: bytes) -> bytes` and `decode(frame: bytes) -> bytes` match that spec exactly — byte-identical frames on encode, and full validation on decode (a frame that violates any rule must raise `FrameError`). Keep the module importable and keep the existing `encode`/`decode`/`FrameError` names and the command-line interface intact.

A handful of known-good `payload -> frame` pairs are in `/app/samples/vectors.json` for you to check against. Do not read or import anything from `/tests` or `/solution`.

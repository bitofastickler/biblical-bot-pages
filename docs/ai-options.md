# Optional AI: deferred until a later release

The core read → reflect → download → reopen loop works without AI. **Decision: ship no AI in version 1.** No owner key, proxy, token field, model download, or inference request is included.

## User-funded hosted AI

Possible only with a provider that explicitly supports browser access (including CORS) or a user-owned endpoint. Users would pay their provider's metered rates; actual cost depends on provider, model, context size, and output length. There is no price commitment or owner-funded fallback. A provider must be selected and its then-current pricing/terms checked before implementation.

Prompts and any included notes or passages would leave the device and be subject to provider retention policies. A browser cannot hide a key from its own scripts, extensions, or a compromised device. A later design should prefer provider-issued short-lived credentials where supported, otherwise explain the risk and keep keys only in memory, never in localStorage or downloaded studies. Restrict destination hosts, show exactly what is being sent, and require explicit opt-in. Do not advise users to paste credentials into notebook text.

## On-device inference

[WebLLM](https://webllm.mlc.ai/docs/) supports browser inference accelerated by WebGPU; its documentation was checked on 2026-10-24. This is technically compatible with a static frontend. It still requires model artifacts and a compatible browser/GPU, sufficient memory and storage, and an initial download. Depending on model choice, downloads can be hundreds of MB to several GB; low-end mobile devices may be unsuitable. There is no per-token API bill, but users bear bandwidth, battery, memory, and compute costs. Model hosting/redistribution and licenses need separate verification.

Prompts can remain on-device once the model loads, but model downloads still contact a host. Test actual offline inference and network behavior before making privacy claims. Capability detection, cancellation, download consent, resource limits, and a fully functional no-AI fallback would be required. No universal minimum RAM/GPU figure is promised before benchmarking a selected model.

Neither approach should quote scripture from model memory. Use the bundled passage as source, link citations into the reader, distinguish commentary from scripture, and validate references. Evaluate usefulness and hallucinations on realistic study questions before choosing either option.

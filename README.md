## Noah Sabbavarapu

AI/ML engineer in Austin, TX.

I'm most interested in the part of the problem that starts *after* the model works — the eval harness that tells you whether it actually improved, the fallback layer that runs when inference stalls, the reward signal that's a proxy for the thing you actually care about. A model that scores well and a system you can trust are different artifacts, and the second one is the harder build.

Lately that's meant fine-tuning and RL on code-generation models, agentic self-correction loops, and benchmark methodology. Before that, medical imaging and embedded control.

---

### Selected work

**[spec2RTL](https://github.com/NoahSabb/spec2RTL)** — Natural language → synthesizable Verilog
A three-stage system on Qwen2.5-Coder-32B: QLoRA supervised fine-tuning, GRPO reinforcement learning against a compiler reward, then an agentic self-correction loop that pairs the tuned generator with a reflector model reading real simulation failures.

Evaluated on CVDP cid003 with the cocotb Docker harness — functional simulation, not syntax checks.

| Stage | cocotb pass@1 |
|---|---|
| Base Qwen2.5-Coder-32B | 14.10% |
| + SFT | 19.23% |
| + GRPO RL | 29.49% |
| + agentic loop | **58.97%** |

**+44.87pp end to end, and +3.84pp over Claude Sonnet 4.6 standalone (55.13%)** — which was the goal. Training data was built by validating 7,525 Verilog modules through iverilog and Verilator, generating specs for each, then filtering with an LLM judge. The reflector went through eleven revisions; v11 regressed by 4 problems and the writeup keeps the regression analysis in rather than quietly dropping it. Weights: [`Noahsabb/spec2rtl-qwen32b-lora-rl-v2`](https://huggingface.co/Noahsabb/spec2rtl-qwen32b-lora-rl-v2).

**[Nexus](https://github.com/Bmohmand/Nexus)** — Packing intelligence for missions, travel, and logistics
Photograph your gear, describe the mission in plain English, get an optimized manifest. GPT-5 Vision extracts structured attributes per item (material, thermal rating, medical use, durability), Voyage `voyage-multimodal-3.5` embeds them into pgvector, and OR-Tools CP-SAT solves a bounded knapsack over the retrieved set — weight limits, category diversity, tag requirements — and reports which constraints it had to relax. Flutter + FastAPI + Supabase.

The interesting part is the split: retrieval is semantic, selection is a hard constraint solver. Asking an LLM to "pick the best items under 40 lbs" gets you plausible arithmetic. A CP-SAT model gets you an answer that's actually feasible.

**[Crucible](https://github.com/KartikeyaGoel/claude_buildathon)** — *Decide with structure, not vibes.* — Claude @ Stanford Buildathon 2026
Anthropic studied 81,000 users and found 37% say AI actively impedes good decisions — the only category where harm outweighed benefit. General-purpose models validate your framing and send you out overconfident.

Crucible runs a decision through four agents with isolated prompts and a grader gating each handoff: a **Framer** you must confirm before anything proceeds, an **Excavator** that drills into unstated assumptions until it hits bedrock, a **Steelman** that argues the opposite case — running concurrently with the Excavator and with *zero* access to its output, so the two perspectives can't anchor on each other — and a **Synthesizer** that only runs once both pass grading. Output carries an explicit confidence percentage and flip conditions: the specific assumptions that, if wrong, reverse the recommendation. Postgres + pgvector, Fastify REST, MCP over Streamable HTTP, deployed on Cloud Run.

**[retinal-ai](https://github.com/Bmohmand/retinal-ai)** — Does the wider retinal view actually help?
Multi-class disease classification comparing 200° ultra-widefield imaging against 45° fundus crops, run across a balanced 700-image set and a larger imbalanced 2,031-image set to keep class imbalance from masquerading as signal. Classical baselines (logistic regression, random forest) on handcrafted features alongside EfficientNet CNNs, with Grad-CAM and occlusion sensitivity to check the models were reading pathology rather than capture artifacts.

**[SMART-GPT2](https://github.com/Tofuwang45/SMART-GPT2)** — Adversarial regularization on GPT-2 fine-tuning
GPT-2 built up from attention and transformer layers, then extended with SMART regularization — smoothness-inducing adversarial perturbation plus Bregman proximal point optimization — ablated four ways (vanilla, smoothness-only, Bregman-only, full) across paraphrase detection and sonnet generation. Stanford CS 224N.

**TeslaCart** — Retrofitting a 2015 Club Car Precedent i2 into a self-driving vehicle *(private)*
Pick a destination on a map; the cart drives there at 8–12 mph, stopping for obstacles and resuming when clear. Imitation learning on driving data collected from the cart itself, fine-tuning SmolVLA and deploying it quantized on a Jetson Orin Nano.

The architecture is three layers that each fail gracefully into the one below: Jetson reasoning at 10–15 Hz, an Arduino Mega enforcing limits at 50 Hz, and relays plus a hardware E-stop with no software in the path. The Jetson is smart but runs a non-real-time OS, so it can't *guarantee* timing; the Arduino is dumb but deterministic. The dumb-but-certain layer sits between the smart layer and anything that can hurt someone. Heartbeat drops, throttle zeroes. E-stop hit, it's a stock golf cart again.

Throttle actuation is road-tested — a DS3502 digital potentiometer impersonating the pedal sensor, swapped in by relay. Steering is a belt drive on the column.

---

### Also

At work I build and evaluate autonomous coding agents — benchmark harnesses, agent reliability, and the certification protocol that decides whether a benchmark's verdicts are trustworthy before anyone acts on its numbers. Recent work included taking one production agent's retry rate from roughly two-in-three down to under 2%.

Elsewhere: **linux-ai**, a kernel fork exploring eBPF subsystems that replace static heuristics with online learning across scheduling, page cache, THP sizing, and NUMA placement — no offline training, no config. Ongoing and speculative. And [EZ-Build](https://github.com/Tofuwang45/EZ-Build), a Unity XR system that tracks physical LEGO assembly through joint-based snap detection and generates step-by-step instructions from the live connection graph.

---

**Austin, TX** · [HuggingFace](https://huggingface.co/Noahsabb)

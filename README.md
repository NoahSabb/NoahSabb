```text
                                           noah@sabbavarapu
                                           ──────────────────────────────────
                    ##%%#                  OS:          macOS 26 Tahoe
             ###%%%%%%#%%%%%%              Host:        Stanford University #GoCardinal
          #%%#%##@@%%%%%%%%%%%%%           Kernel:      <your major>
         ##%%%%%%##***%%%%%%%%%@           Shell:       AI/ML Engineer
        #%%%#%++-.   :*##%%@%%%%%          Location:    Austin, TX
        ##%##-        .::-==#@%%%%
        #%%%::--=--   :----=-#@@@          Languages:   Python, C/C++, Verilog, Dart, TS
         #%= .::=--  .--+---:+%=           ML Stack:    PyTorch, QLoRA, GRPO, vLLM
         =::     .   .... .:-+-:           Focus:       LLM post-training, agent evals
          .::..::....::.:..-+-.            Hobbies:     <fill in>
            -:::::..:::--:-=*
             -:......::-.:==*              Contact
              =-.  ....:-++*%%             ──────────────────────────────────
               -=---:-=*##%%%%%            Email:       noah.sabb@gmail.com
             %@=::-=*#%%%%%%%%%%#          School:      noahsabb@stanford.edu
           ###%%*##%%####%%%#*++*###%%     LinkedIn:    <fill in>
           %##%@@%#######*+==--==**###%    Portfolio:   <fill in>
                                           HuggingFace: huggingface.co/Noahsabb
```

I work on the part of the problem that starts *after* the model works — the eval harness
that tells you whether a change actually helped, the fallback layer for when inference
stalls, the reward signal that only stands in for the thing you care about. A model that
scores well and a system you can trust are different artifacts, and the second is the
harder build. Lately that has meant post-training code-generation models and writing the
certification protocol that decides whether a benchmark's verdicts can be trusted at all;
day to day I build and evaluate autonomous coding agents, which recently included taking
one production agent's retry rate from roughly two-in-three down to under 2%. Before that,
medical imaging and embedded control. Most of my work lives in private repos, so this
profile is quieter than my commit history — happy to talk about any of it.

### Selected work

**[spec2RTL](https://github.com/NoahSabb/spec2RTL)** — Natural language → synthesizable
Verilog. Three stages on Qwen2.5-Coder-32B: QLoRA supervised fine-tuning, GRPO
reinforcement learning against a compiler reward, then an agentic self-correction loop
pairing the tuned generator with a reflector model that reads real simulation failures.
**14.10% → 58.97% cocotb pass@1** on CVDP cid003, beating Claude Sonnet 4.6 standalone by
+3.84pp. Training data came from 7,525 Verilog modules validated through iverilog and
Verilator. Weights: [`spec2rtl-qwen32b-lora-rl-v2`](https://huggingface.co/Noahsabb/spec2rtl-qwen32b-lora-rl-v2).

**[Nexus](https://github.com/Bmohmand/Nexus)** — Photograph your gear, describe the mission
in plain English, get an optimized packing manifest. GPT-5 Vision extracts structured
attributes, Voyage multimodal embeddings land in pgvector, and OR-Tools CP-SAT solves a
bounded knapsack over the retrieved set. Retrieval is semantic; selection is a hard
constraint solver — ask an LLM to "pick the best items under 40 lbs" and you get plausible
arithmetic instead of a feasible answer.

**[Crucible](https://github.com/KartikeyaGoel/claude_buildathon)** — Decision support that
argues back. Four agents with isolated prompts and a grader gating every handoff; the
Steelman runs concurrently with the Excavator and blind to its output, so the two
perspectives can't anchor on each other. Output carries explicit flip conditions — the
assumptions that, if wrong, reverse the recommendation. Built at the Claude @ Stanford
Buildathon 2026.

**[retinal-ai](https://github.com/Bmohmand/retinal-ai)** — Does the wider retinal view
actually help? Multi-class disease classification comparing 200° ultra-widefield imaging
against 45° fundus crops, run across balanced and imbalanced sets so class imbalance can't
masquerade as signal. EfficientNet CNNs alongside classical baselines, with Grad-CAM and
occlusion sensitivity confirming the models read pathology rather than capture artifacts.

**[SMART-GPT2](https://github.com/Tofuwang45/SMART-GPT2)** — GPT-2 built up from attention
and transformer layers, then extended with SMART adversarial regularization — smoothness
perturbation plus Bregman proximal point — ablated four ways across paraphrase detection
and sonnet generation. Stanford CS 224N.

**TeslaCart** *(private)* — Retrofitting a 2015 Club Car into a self-driving vehicle.
SmolVLA fine-tuned on driving data collected from the cart itself, quantized onto a Jetson
Orin Nano. Three layers that each fail gracefully into the one below: Jetson reasoning at
10–15 Hz, an Arduino Mega enforcing limits at 50 Hz, and relays plus a hardware E-stop
with no software in the path. Throttle actuation is road-tested.

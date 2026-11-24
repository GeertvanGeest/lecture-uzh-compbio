# Vevox questions — BIO390, 1 Dec 2026

Questions are grouped by the `Question` slide where they are asked. ✅ marks the correct answer for knowledge questions. Background questions have no correct answer.

---

## Block 1: start of lecture (slide "Questions!")

### Q1 — Background: study programme
**What kind of programme are you in?** (single choice)

- BSc Biology / Life Sciences
- MSc Biology / Life sciences (e.g. Biochemistry, Biomedicine, Molecular Life Sciences)
- BSc Computer Science / Data Science
- MSc Computer Science/ Data Science
- PhD programme
- Other

### Q2 — Background: programming experience
**How familiar are you with programming / the command line?** (single choice)

- Not familiar: I use programs with a graphical interface
- I've had an introductory course and am getting familiar
- I regularly write code (R, Python, bash…) for my studies or research
- I consider myself a (computational) bioinformatician / developer

### Q3 — Pre-lecture knowledge: FAIR awareness
**What do you know about the FAIR principles?** (single choice)

- Never heard of them
- Heard of them, but couldn't say what the letters stand for
- I can name the four principles
- I actively apply them in my own work

### Q4 — Pre-lecture knowledge: databases
**Which of these resources have you used before?** (multiple choice)

- UniProt
- Protein Data Bank (PDB) / AlphaFold DB
- NCBI (GenBank, PubMed, BLAST…) or Ensembl
- STRING
- Expasy (or another SIB resource, e.g. SWISS-MODEL, Bgee)
- None of these

### Q5 — Background: version control with git
**How experienced are you with git?** (single choice)

- I have never heard of it
- I know what it is, but have never used it
- I have used it a few times (e.g. in a course)
- I use it regularly (commit, push, pull)
- I use branches, pull requests and collaborate via GitHub/GitLab

*Use the answers to decide how much to explain on the slides that assume git: "The toolbox", "FAIR applies to software", "Working with agents: do's and don'ts" (commit, `git diff`) and "AI and reproducibility" (commit AI-generated code, review the diff).*

---

## Block 2: after "FAIR data and AI"

### Q6 — Which resource has its roots at SIB / in Switzerland?
(single choice)

- GenBank
- UniProtKB/Swiss-Prot ✅
- Protein Data Bank (PDB)
- Ensembl

*Explanation: Swiss-Prot was started in Geneva in 1986 and became part of UniProt in 2002. GenBank (NCBI, USA), PDB (wwPDB, founded in the US in 1971) and Ensembl (EMBL-EBI/Sanger, UK) are not.*

### Q7 — True or false: "FAIR data must be openly available to everyone."
(single choice)

- True
- False ✅

*Explanation: "As open as possible, as closed as necessary". Sensitive data can be FAIR with public metadata and controlled access (e.g. EGA, BioMedIT).*

### Q8 — Which of these contributes MOST to making a dataset useful for training an AI model?
(single choice)

- Storing it as a PDF table in the supplementary material
- Using standard formats, persistent identifiers and ontology terms in the metadata ✅
- Making the file as small as possible
- Sending it to anyone who asks by e-mail

### Q9 — Guess: in an audit of ~2,900 human microbiome studies (2012–2025), what share deposited sequence data with per-sample disease status, age and sex?
(single choice; ask *before* showing the slide "Shared ≠ reusable")

- About 6% ✅
- About 25%
- About 50%
- About 80%

*Explanation: 5.9% (Tier 1); 63.1% shared no reusable sequence data at all, so 85.5% of ~720,000 samples cannot be reused without contacting the authors, and this did not improve over the decade. Degregori et al. (2026) iMeta e70192, https://doi.org/10.1002/imt2.70192*

---

## Block 3: after "Reproducible analyses"

### Q10 — You rerun your own analysis from two years ago on the same data and get different results. What is the most likely cause?
(single choice)

- Different versions of software packages / reference annotations ✅
- The raw data files have changed by themselves
- Computers calculate differently over time
- The original results were fraudulent

*Discussion: random seeds and undocumented manual steps are other common culprits. Environments (conda, containers) and workflows address these.*

### Q11 — Which of these is a workflow manager?
(single choice)

- Zenodo
- Quarto
- Nextflow ✅
- Conda

*Explanation: Zenodo = repository/DOI, Quarto = literate programming, Conda = environment/package manager.*

---

## Block 4: start of "AI in the bioinformatician's daily work" (after the break)

### Q12 — Background: How do you use AI tools (ChatGPT, Claude, Copilot, …) for coding or data analysis?
(single choice)

- I don't use them
- Occasionally, to ask questions or explain errors
- Regularly, to generate code that I then run
- I use coding agents that edit and run code for me

### Q13 — Background: When an AI tool generates code that runs without errors, how often do you check it line by line?
(single choice)

- Always
- Most of the time
- Rarely
- Never: if it runs, it works
- I don't use AI-generated code

---

## Block 5: after "MCP servers for life science data"

### Q14 — Which description fits an LLM agent best?
(single choice)

- A chatbot that answers from what it learned during training
- An LLM that calls tools in a loop, using the results to decide its next step, until a goal is reached ✅
- A language model trained only on protein sequences
- A human expert who checks the output of an LLM

### Q15 — What does an MCP server do?
(single choice)

- It trains a new LLM on your data
- It exposes tools and data (e.g. a database API) in a standard way so any LLM application can use them ✅
- It guarantees that the LLM's answers are correct
- It stores your chat history in the cloud

*Discussion: an MCP server is only as good as the API and data behind it. FAIR, machine-actionable resources make good MCP servers possible, but the LLM can still call the wrong tool or misread the result.*

---

## Block 6: slide "Spot the problem"

### Q16 — Spot the problem (code shown on the slide "Spot the problem")
**What is wrong with this differential expression analysis?** (single choice)

- Counts are not normalised for library size
- A t-test on raw counts with few replicates is inappropriate
- There is no multiple testing correction
- All of the above ✅

*Explanation: with ~20,000 genes and p < 0.05, ~1,000 genes are expected to be "significant" by chance alone. Use dedicated tools (DESeq2, edgeR, limma) and adjusted p-values.*

---

## Block 7: end of lecture

### Q17 — Word cloud (open text)
**Which skill do you think will be most important for a bioinformatician in 5 years?** (press "Send" after each entry)

### Q18 — End-of-lecture check: What does the "I" in FAIR stand for?
(single choice)

- Integrated
- Interoperable ✅
- Indexed
- Intelligent

*Optional: re-ask Q3 to see how the room's self-assessment shifted.*

---

### Spare questions (use if time allows)

**Which of these is the best way to refer to a gene in a supplementary table?**

- Its gene symbol, typed in Excel
- A stable identifier such as an Ensembl or HGNC ID ✅
- The protein name as written in the paper
- The chromosome position

**What does a DOI from Zenodo give your code or dataset?**

- A persistent identifier that makes it citable ✅
- Automatic peer review
- A guarantee that the code is correct
- Free cloud computing

**An AI assistant suggests `pip install` of a package you've never heard of. What should you do first?**

- Install it, the AI knows best
- Check that the package exists, is maintained and is what it claims to be ✅
- Ask the AI whether it is sure
- Install it in your base environment so all projects can use it

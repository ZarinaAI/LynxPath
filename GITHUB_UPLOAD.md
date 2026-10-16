# Publish LynxPath v0.1 to GitHub

1. Create an empty public repository named `LynxPath`.
2. Replace `YOUR_USERNAME` in `CITATION.cff` after the repository exists.
3. From this folder:

```bash
git init
git add .
git commit -m "LynxPath v0.1: open capacity schema and reproducible demo"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/LynxPath.git
git push -u origin main
```

4. In GitHub, add labels such as:

- `good first issue`
- `scenario`
- `adapter`
- `interoperability`
- `research`
- `frontend`

5. Open the five issue ideas from `docs/GOOD_FIRST_ISSUES.md` so the repository visibly invites contributions.

6. Test the public instructions from a clean checkout:

```bash
docker compose up --build
```

Then open `http://localhost:8501` and run the fracture timeline from T=0 to T=30.

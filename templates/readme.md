1. **Setup**
- ensure deps are installed (uv preferred)

2. **Create content:**
- add dirs under `content/`
- each dir needs a `config.yml` and `content.yml`
  - use cookiecutter or copier to make this happen
3. **Process all docs**
  ```bash
  # Process all docs
  python templating_app.py batch
  ```

  ```
  # Process single file
  python templating_app.py content/music_theory_cheatsheet_12_10_25
  ```

4. **Customize templates:**
   - Edit templates in `templates/base/`
   - Modify styles in `templates/styles/`
   - Update global config in `config/global.yaml
```
```

```
```

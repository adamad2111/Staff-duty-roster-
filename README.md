# Duty Roster

A simple, mobile-friendly weekly duty roster for doctors and staff. Add staff with designations, define your own shifts, and assign them day by day. The week runs Sunday to Saturday.

Built with Python (generates the page), HTML, CSS and JavaScript. No frameworks, no server, no dependencies.

## Features
- Add and remove staff, each with a designation
- Create shifts with a code, name, hours and colour
- Weekly roster view (day by day) and an assign-shifts grid
- Print, export the week to CSV, clear a week
- Responsive layout and automatic dark mode
- Data is saved in your browser (localStorage)

## Run it
1. Open `index.html` in any browser. That is all.
2. To change the default designations or shifts, edit `DEFAULTS` in `generate_roster.py`, then run:

```bash
python generate_roster.py
```

This rewrites `index.html`. Requires Python 3.

## Publish on GitHub Pages
1. Push this folder to a GitHub repository.
2. Go to Settings, then Pages, choose the `main` branch and the root folder, and save.
3. Your roster will be live at `https://<your-username>.github.io/<repo-name>/`.

Data is stored per browser and device. Use Export CSV to keep a copy.

## License
MIT

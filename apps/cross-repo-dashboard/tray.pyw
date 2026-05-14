"""Cross-repo Dashboard system tray launcher v0.2 (A4).

Runs Flask app in background thread + shows system tray icon.
Right-click menu: Open Dashboard / Force Refresh / Quit.

Usage: pythonw tray.pyw (windowless background)
"""

from __future__ import annotations

import threading
import webbrowser
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError as e:
    import sys
    print(f"Missing dep: {e}. Install: pip install pystray Pillow")
    sys.exit(1)

# Import Flask app + waitress
import app as flask_app  # noqa: E402

DASHBOARD_URL = "http://127.0.0.1:8081/"
ICON_SIZE = (64, 64)


def make_icon_image() -> Image.Image:
    """Create simple dashboard icon (no external file needed)."""
    img = Image.new("RGB", ICON_SIZE, color=(13, 17, 23))  # GitHub dark bg
    draw = ImageDraw.Draw(img)
    # Draw 4 mini-cards 2x2 grid
    cards = [
        (8, 8, 28, 28, (88, 166, 255)),    # blue
        (36, 8, 56, 28, (188, 140, 255)),  # purple
        (8, 36, 28, 56, (46, 160, 67)),    # green
        (36, 36, 56, 56, (210, 153, 34)),  # amber
    ]
    for x1, y1, x2, y2, color in cards:
        draw.rectangle([x1, y1, x2, y2], fill=color)
    return img


def open_dashboard(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    webbrowser.open(DASHBOARD_URL)


def force_refresh(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    webbrowser.open(DASHBOARD_URL + "?refresh=1")


def quit_app(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    icon.stop()
    # Server background thread daemon will die with main process


def run_flask_background() -> None:
    """Run Flask via waitress in daemon thread (so quit kills it)."""
    try:
        from waitress import serve
        serve(flask_app.app, host="127.0.0.1", port=8081, threads=4)
    except ImportError:
        # Fallback to Werkzeug dev server
        flask_app.app.run(host="127.0.0.1", port=8081, debug=False, threaded=False)


def main() -> None:
    # Start Flask in background daemon thread
    flask_thread = threading.Thread(target=run_flask_background, daemon=True)
    flask_thread.start()

    # Build tray icon
    icon = pystray.Icon(
        name="cross-repo-dashboard",
        icon=make_icon_image(),
        title="Cross-repo Dashboard v0.2",
        menu=pystray.Menu(
            pystray.MenuItem("Open Dashboard", open_dashboard, default=True),
            pystray.MenuItem("Force Refresh", force_refresh),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", quit_app),
        ),
    )
    icon.run()


if __name__ == "__main__":
    main()

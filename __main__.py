from __future__ import annotations

import sys
from pathlib import Path

from .settings_manager import get_settings, JarvisSettings


def show_startup_dialog() -> bool:
    """Show a startup dialog asking if user wants to enable Slint UI."""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        result = messagebox.askyesno(
            "Jarvis Startup",
            "Do you want to use the modern Slint UI?\n\n"
            "Yes = Modern Slint UI (recommended)\n"
            "No = Classic Tkinter UI",
            icon=messagebox.QUESTION
        )
        root.destroy()
        return result
    except Exception as e:
        print(f"Dialog error: {e}, defaulting to Tkinter UI")
        return False


def main() -> None:
    """Main entry point with UI selection and settings management."""
    try:
        from .paths import ensure_directories
        from .settings_manager import get_settings

        ensure_directories()

        # Load settings
        settings = get_settings()

        # Validate settings
        valid, error_msg = settings.validate()
        if not valid:
            print(f"Warning: {error_msg}")

        # Determine which UI to use
        use_slint = settings.ui.enabled_on_startup

        # If not explicitly set, show dialog once
        if not use_slint:
            use_slint = show_startup_dialog()
            settings.ui.enabled_on_startup = use_slint
            settings.save()

        # Launch the appropriate UI
        if use_slint:
            try:
                print("Launching modern Slint UI...")
                from .slint_ui import JarvisSlintWindow
                app = JarvisSlintWindow(settings)
                app.run()
            except ImportError:
                print("Slint not available, falling back to Tkinter UI")
                from .ui import JarvisWindow
                app = JarvisWindow()
                app.run()
            except Exception as e:
                print(f"Error in Slint UI: {e}, falling back to Tkinter")
                from .ui import JarvisWindow
                app = JarvisWindow()
                app.run()
        else:
            print("Launching classic Tkinter UI...")
            from .ui import JarvisWindow
            app = JarvisWindow()
            app.run()

    except KeyboardInterrupt:
        print("\nJarvis shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

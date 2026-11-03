"""Show Sami's completed battle result for five seconds using Tkinter."""


def show_result(result, seconds=5):
    """Display results, then close automatically; fall back to text if no GUI."""
    if result is None:
        return
    try:
        import tkinter as tk
        from tkinter import ttk

        window = tk.Tk()
        window.title('Dungeon Brawler - Combat Result')
        window.geometry('420x275')
        window.resizable(False, False)
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='VICTORY' if result.success else 'DEFEAT',
                  font=('Arial', 20, 'bold')).pack(pady=(0, 10))
        ttk.Label(frame, text=f'Door: {result.door}').pack()
        ttk.Label(frame, text=result.reason, wraplength=370).pack(pady=8)
        ttk.Label(frame, text='Renown: ' + ', '.join(
            f'{name} +{score}' for name, score in result.renown.items())).pack(pady=4)
        ttk.Label(frame, text='Coins: ' + ', '.join(
            f'{name} +{coins}' for name, coins in result.coins.items())).pack(pady=4)
        ttk.Label(frame, text=f'Closing automatically in {seconds:g} seconds…').pack(pady=12)
        window.after(max(0, int(seconds * 1000)), window.destroy)
        window.mainloop()
    except Exception as error:
        # Headless systems may not have a display; combat results still return.
        print(f'Results window unavailable ({error}). Combat result returned.')

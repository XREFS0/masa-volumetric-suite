"""
MASA Volumetric & Fluid Dynamics Precision Converter
Developer: MASA
"""

import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MasaVolumeConverter(ctk.CTk):
    # Base reference: 1 Liter (L)
    UNIT_FACTORS = {
        "Liter (L)": 1.0,
        "Milliliter (mL / cc)": 0.001,
        "Cubic Meter (m³)": 1000.0,
        "Cubic Foot (cu ft)": 28.3168,
        "Cubic Inch (cu in)": 0.0163871,
        "US Liquid Gallon": 3.78541,
        "US Liquid Quart": 0.946353,
        "US Liquid Pint": 0.473176,
        "US Legal Cup": 0.24,
        "Fluid Ounce (fl oz)": 0.0295735,
        "Tablespoon (US tbsp)": 0.0147868,
        "Teaspoon (US tsp)": 0.00492892,
        "Imperial Gallon (UK)": 4.54609,
    }

    def __init__(self):
        super().__init__()

        self.title("MASA Volumetric Engine")
        self.geometry("480x560")
        self.resizable(False, False)
        self.configure(fg_color="#0A0E17")

        self.unit_names = list(self.UNIT_FACTORS.keys())
        self.from_unit = ctk.StringVar(value="Liter (L)")
        self.to_unit = ctk.StringVar(value="US Liquid Gallon")

        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#121826", corner_radius=14)
        header.pack(fill="x", padx=20, pady=(20, 15))

        title = ctk.CTkLabel(
            header,
            text="MASA VOLUMETRIC SUITE",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color="#10B981",
        )
        title.pack(pady=(12, 2))

        subtitle = ctk.CTkLabel(
            header,
            text="Fluid Mechanics & Metric-Imperial Volume Matrix",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8",
        )
        subtitle.pack(pady=(0, 12))

        calc_card = ctk.CTkFrame(self, fg_color="#121826", corner_radius=16)
        calc_card.pack(fill="x", padx=20, pady=5)

        lbl_val = ctk.CTkLabel(calc_card, text="SOURCE QUANTITY", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8")
        lbl_val.pack(anchor="w", padx=16, pady=(15, 2))

        self.entry_amount = ctk.CTkEntry(
            calc_card,
            placeholder_text="1.0",
            font=ctk.CTkFont(family="Consolas", size=16),
            height=40,
            corner_radius=10,
        )
        self.entry_amount.pack(fill="x", padx=16, pady=(0, 12))
        self.entry_amount.insert(0, "1")
        self.entry_amount.bind("<KeyRelease>", lambda _: self._calculate())

        units_grid = ctk.CTkFrame(calc_card, fg_color="transparent")
        units_grid.pack(fill="x", padx=16, pady=(0, 15))
        units_grid.grid_columnconfigure(0, weight=1)
        units_grid.grid_columnconfigure(1, weight=1)

        lbl_from = ctk.CTkLabel(units_grid, text="FROM UNIT", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8")
        lbl_from.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.menu_from = ctk.CTkOptionMenu(
            units_grid,
            values=self.unit_names,
            variable=self.from_unit,
            command=lambda _: self._calculate(),
            fg_color="#059669",
            button_color="#047857",
            corner_radius=8,
        )
        self.menu_from.grid(row=1, column=0, sticky="ew", padx=(0, 6))

        lbl_to = ctk.CTkLabel(units_grid, text="TO UNIT", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8")
        lbl_to.grid(row=0, column=1, sticky="w", pady=(0, 2))

        self.menu_to = ctk.CTkOptionMenu(
            units_grid,
            values=self.unit_names,
            variable=self.to_unit,
            command=lambda _: self._calculate(),
            fg_color="#059669",
            button_color="#047857",
            corner_radius=8,
        )
        self.menu_to.grid(row=1, column=1, sticky="ew", padx=(6, 0))

        display_card = ctk.CTkFrame(self, fg_color="#121826", corner_radius=16)
        display_card.pack(fill="both", expand=True, padx=20, pady=(12, 20))

        self.lbl_result = ctk.CTkLabel(
            display_card,
            text="0.264172",
            font=ctk.CTkFont(family="Consolas", size=36, weight="bold"),
            text_color="#34D399",
        )
        self.lbl_result.pack(pady=(25, 4))

        self.lbl_formula = ctk.CTkLabel(
            display_card,
            text="1 Liter (L) = 0.264172 US Liquid Gallon",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8",
        )
        self.lbl_formula.pack(pady=(0, 20))

        btn_swap = ctk.CTkButton(
            display_card,
            text="⇄ Swap Units",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            corner_radius=8,
            command=self._swap_units,
        )
        btn_swap.pack(side="bottom", pady=15)

        self._calculate()

    def _swap_units(self):
        f = self.from_unit.get()
        t = self.to_unit.get()
        self.from_unit.set(t)
        self.to_unit.set(f)
        self._calculate()

    def _calculate(self):
        raw = self.entry_amount.get().strip()
        if not raw:
            self.lbl_result.configure(text="0")
            return

        try:
            val = float(raw)
        except ValueError:
            self.lbl_result.configure(text="Invalid Input")
            return

        from_factor = self.UNIT_FACTORS[self.from_unit.get()]
        to_factor = self.UNIT_FACTORS[self.to_unit.get()]

        liters = val * from_factor
        converted = liters / to_factor

        formatted = f"{converted:.6g}"
        self.lbl_result.configure(text=formatted)
        self.lbl_formula.configure(text=f"{val:g} {self.from_unit.get()} = {formatted} {self.to_unit.get()}")


if __name__ == "__main__":
    app = MasaVolumeConverter()
    app.mainloop()

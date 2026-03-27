// =============================================================
// PhysicsConverter — Native macOS app (Cocoa / AppKit)
// Conventions: SI · Imperial · CGS · Natural/Planck
// Author : Ayas O.
// Created at : 21:45 27 mars Ven. 2026
// Localizaion : Macbook air, Chrome, Github
// RWA Localization : ECS 72*** FR
// File INTENT : receiving 1200€/month independant beneficial annuities
// Compile: clang -framework Cocoa unit_converter.m -o unit_converter
// Run: ./unit_converter
// =============================================================
#import <Cocoa/Cocoa.h>
#import <math.h>
// ─────────────────────────────────────────────────────────────
// Physical constants (SI)
// ─────────────────────────────────────────────────────────────
#define C_LIGHT 2.99792458e8 // m/s
#define HBAR 1.054571817e-34 // J·s (ħ)
#define G_NEWTON 6.67430e-11 // m³/(kg·s²)
#define K_BOLTZMANN 1.380649e-23 // J/K
#define E_CHARGE 1.602176634e-19 // C
// Planck units (derived)
#define PLANCK_LENGTH 1.616255e-35 // m
#define PLANCK_MASS 2.176434e-8 // kg
#define PLANCK_TIME 5.391247e-44 // s
#define PLANCK_TEMP 1.416784e32 // K
#define PLANCK_ENERGY 1.956082e9 // J (= Planck mass x c^2)
// ─────────────────────────────────────────────────────────────
// Unit table structure
// ─────────────────────────────────────────────────────────────
typedef struct {
 const char *name;
 const char *convention; // "SI" | "Imperial" | "CGS" | "Natural"
 double toSI; // multiply by this to get SI base unit
} Unit;
// ─────────────────────────────────────────────────────────────
// LENGTH (SI base: metre)
// ─────────────────────────────────────────────────────────────
static Unit lengthUnits[] = {
 // SI
 {"Metre (m)", "SI", 1.0},
 {"Kilometre (km)", "SI", 1e3},
 {"Centimetre (cm)", "SI", 1e-2},
 {"Millimetre (mm)", "SI", 1e-3},
 {"Micrometre (um)", "SI", 1e-6},
 {"Nanometre (nm)", "SI", 1e-9},
 {"Picometre (pm)", "SI", 1e-12},
 // Imperial
 {"Mile (mi)", "Imperial", 1609.344},
 {"Furlong", "Imperial", 201.168},
 {"Chain", "Imperial", 20.1168},
 {"Yard (yd)", "Imperial", 0.9144},
 {"Foot (ft)", "Imperial", 0.3048},
 {"Inch (in)", "Imperial", 0.0254},
 {"Thou (mil)", "Imperial", 2.54e-5},
 {"Nautical mile", "Imperial", 1852.0},
 // CGS
 {"Angstrom (A)", "CGS", 1e-10},
 {"Fermi (fm)", "CGS", 1e-15},
 // Natural / Planck
 {"Planck length (lp)", "Natural", PLANCK_LENGTH},
 {"Bohr radius (a0)", "Natural", 5.29177210903e-11},
 {"Light-second", "Natural", C_LIGHT},
 {"Light-year (ly)", "Natural", 9.4607304725808e15},
 {"Parsec (pc)", "Natural", 3.085677581e16},
 {NULL, NULL, 0}
};
// ─────────────────────────────────────────────────────────────
// MASS (SI base: kilogram)
// ─────────────────────────────────────────────────────────────
static Unit massUnits[] = {
 // SI
 {"Kilogram (kg)", "SI", 1.0},
 {"Gram (g)", "SI", 1e-3},
 {"Milligram (mg)", "SI", 1e-6},
 {"Microgram (ug)", "SI", 1e-9},
 {"Tonne (t)", "SI", 1e3},
 {"Kilotonne (kt)", "SI", 1e6},
 // Imperial
 {"Pound (lb)", "Imperial", 0.45359237},
 {"Ounce (oz)", "Imperial", 0.028349523125},
 {"Stone (st)", "Imperial", 6.35029318},
 {"Slug", "Imperial", 14.593903},
 {"Short ton (US)", "Imperial", 907.18474},
 {"Long ton (UK)", "Imperial", 1016.0469},
 {"Grain (gr)", "Imperial", 6.479891e-5},
 // CGS
 {"Gram (g) CGS", "CGS", 1e-3},
 {"Milligram (mg) CGS", "CGS", 1e-6},
 // Natural / Planck
 {"Planck mass (mp)", "Natural", PLANCK_MASS},
 {"Atomic mass unit (u)", "Natural", 1.66053906660e-27},
 {"Electron mass (me)", "Natural", 9.1093837015e-31},
 {"Proton mass (mpr)", "Natural", 1.67262192369e-27},
 {"Solar mass (Msun)", "Natural", 1.989e30},
 {NULL, NULL, 0}
};
// ─────────────────────────────────────────────────────────────
// SPEED (SI base: m/s)
// ─────────────────────────────────────────────────────────────
static Unit speedUnits[] = {
 // SI
 {"m/s", "SI", 1.0},
 {"km/h", "SI", 1.0/3.6},
 {"km/s", "SI", 1e3},
 // Imperial
 {"mph", "Imperial", 0.44704},
 {"ft/s", "Imperial", 0.3048},
 {"ft/min", "Imperial", 0.00508},
 {"Knot (kn)", "Imperial", 0.514444},
 // CGS
 {"cm/s", "CGS", 1e-2},
 // Natural / Planck
 {"Speed of light (c)", "Natural", C_LIGHT},
 {"Mach (sea level)", "Natural", 340.29},
 {"Escape velocity Earth", "Natural", 11186.0},
 {"Escape velocity Sun", "Natural", 617700.0},
 {NULL, NULL, 0}
};
// ─────────────────────────────────────────────────────────────
// PRESSURE (SI base: Pascal)
// ─────────────────────────────────────────────────────────────
static Unit pressureUnits[] = {
 // SI
 {"Pascal (Pa)", "SI", 1.0},
 {"Kilopascal (kPa)", "SI", 1e3},
 {"Megapascal (MPa)", "SI", 1e6},
 {"Gigapascal (GPa)", "SI", 1e9},
 {"Millibar (mbar)", "SI", 1e2},
 {"Bar", "SI", 1e5},
 // Imperial
 {"psi (lbf/in2)", "Imperial", 6894.757},
 {"ksi (kip/in2)", "Imperial", 6.894757e6},
 {"Atmosphere (atm)", "Imperial", 101325.0},
 {"mmHg (Torr)", "Imperial", 133.32236842},
 {"inHg", "Imperial", 3386.389},
 {"inH2O", "Imperial", 249.0889},
 // CGS
 {"Barye (Ba)", "CGS", 0.1},
 {"cmHg", "CGS", 1333.22},
 // Natural / Planck
 {"Planck pressure", "Natural", 4.63309e113},
 {NULL, NULL, 0}
};
// ─────────────────────────────────────────────────────────────
// ENERGY (SI base: Joule)
// ─────────────────────────────────────────────────────────────
static Unit energyUnits[] = {
 // SI
 {"Joule (J)", "SI", 1.0},
 {"Kilojoule (kJ)", "SI", 1e3},
 {"Megajoule (MJ)", "SI", 1e6},
 {"Gigajoule (GJ)", "SI", 1e9},
 {"Watt-hour (Wh)", "SI", 3600.0},
 {"Kilowatt-hour (kWh)", "SI", 3.6e6},
 {"Megawatt-hour (MWh)", "SI", 3.6e9},
 // Imperial
 {"BTU (IT)", "Imperial", 1055.05585},
 {"Therm (US)", "Imperial", 1.054804e8},
 {"Foot-pound (ft.lbf)", "Imperial", 1.3558179483},
 {"Calorie (cal)", "Imperial", 4.184},
 {"Kilocalorie (kcal)", "Imperial", 4184.0},
 // CGS
 {"Erg", "CGS", 1e-7},
 {"Dyne-centimetre", "CGS", 1e-7},
 // Natural / Planck
 {"Electron-volt (eV)", "Natural", E_CHARGE},
 {"Kiloelectron-volt (keV)","Natural", E_CHARGE * 1e3},
 {"Megaelectron-volt (MeV)","Natural", E_CHARGE * 1e6},
 {"Gigaelectron-volt (GeV)","Natural", E_CHARGE * 1e9},
 {"Teraelectron-volt (TeV)","Natural", E_CHARGE * 1e12},
 {"Planck energy (Ep)", "Natural", PLANCK_ENERGY},
 {"Hartree (Eh)", "Natural", 4.3597447222071e-18},
 {NULL, NULL, 0}
};
// ─────────────────────────────────────────────────────────────
// TEMPERATURE — offset math, handled separately
// ─────────────────────────────────────────────────────────────
typedef struct { const char *name; const char *convention; } TempUnit;
static TempUnit tempUnits[] = {
 {"Celsius (degC)", "SI"},
 {"Kelvin (K)", "SI"},
 {"Fahrenheit (degF)", "Imperial"},
 {"Rankine (degR)", "Imperial"},
 {"Reaumur (degRe)", "CGS"},
 {"Delisle (degDe)", "CGS"},
 {"Newton (degN)", "CGS"},
 {"Romer (degRo)", "CGS"},
 {"Planck temp (Tp)", "Natural"},
 {NULL, NULL}
};
static double convertTemp(int from, int to, double v) {
 double c;
 switch (from) {
 case 0: c = v; break;
 case 1: c = v - 273.15; break;
 case 2: c = (v - 32.0) * 5.0/9.0; break;
 case 3: c = (v - 491.67) * 5.0/9.0; break;
 case 4: c = v * 1.25; break;
 case 5: c = 100.0 - v * 2.0/3.0; break;
 case 6: c = v * 100.0/33.0; break;
 case 7: c = (v - 7.5) * 40.0/21.0; break;
 case 8: c = v * PLANCK_TEMP - 273.15; break;
 default: c = v;
 }
 switch (to) {
 case 0: return c;
 case 1: return c + 273.15;
 case 2: return c * 9.0/5.0 + 32.0;
 case 3: return (c + 273.15) * 9.0/5.0;
 case 4: return c * 0.8;
 case 5: return (100.0 - c) * 1.5;
 case 6: return c * 33.0/100.0;
 case 7: return c * 21.0/40.0 + 7.5;
 case 8: return (c + 273.15) / PLANCK_TEMP;
 default: return c;
 }
}
// ─────────────────────────────────────────────────────────────
// Category registry
// ─────────────────────────────────────────────────────────────
#define CAT_LENGTH 0
#define CAT_MASS 1
#define CAT_SPEED 2
#define CAT_PRESSURE 3
#define CAT_ENERGY 4
#define CAT_TEMPERATURE 5
#define CAT_COUNT 6
static const char *categoryNames[CAT_COUNT] = {
 "Length / Distance",
 "Mass / Weight",
 "Speed / Velocity",
 "Pressure",
 "Energy / Power",
 "Temperature"
};
static Unit *unitTables[CAT_COUNT] = {
 lengthUnits, massUnits, speedUnits, pressureUnits, energyUnits, NULL
};
static int unitCount(int cat) {
 if (cat == CAT_TEMPERATURE) {
 int n = 0; while (tempUnits[n].name) n++; return n;
 }
 int n = 0; while (unitTables[cat][n].name) n++; return n;
}
static const char *unitName(int cat, int idx) {
 if (cat == CAT_TEMPERATURE) return tempUnits[idx].name;
 return unitTables[cat][idx].name;
}
static const char *unitConvention(int cat, int idx) {
 if (cat == CAT_TEMPERATURE) return tempUnits[idx].convention;
 return unitTables[cat][idx].convention;
}
static double doConvert(int cat, int from, int to, double value) {
 if (from == to) return value;
 if (cat == CAT_TEMPERATURE) return convertTemp(from, to, value);
 double si = value * unitTables[cat][from].toSI;
 return si / unitTables[cat][to].toSI;
}
// ─────────────────────────────────────────────────────────────
// Convention badge colours
// ─────────────────────────────────────────────────────────────
static NSColor *conventionColor(NSString *conv) {
 if ([conv isEqualToString:@"SI"]) return [NSColor colorWithCalibratedRed:0.20 green
 if ([conv isEqualToString:@"Imperial"]) return [NSColor colorWithCalibratedRed:1.00 green if ([conv isEqualToString:@"CGS"]) return [NSColor colorWithCalibratedRed:0.40 green if ([conv isEqualToString:@"Natural"]) return [NSColor colorWithCalibratedRed:0.85 green return [NSColor whiteColor];
}
// ─────────────────────────────────────────────────────────────
// App delegate
// ─────────────────────────────────────────────────────────────
@interface AppDelegate : NSObject <NSApplicationDelegate>
@property (strong) NSWindow *window;
@property (strong) NSPopUpButton *categoryPop;
@property (strong) NSPopUpButton *fromPop;
@property (strong) NSPopUpButton *toPop;
@property (strong) NSTextField *inputField;
@property (strong) NSTextField *resultField;
@property (strong) NSTextField *formulaLabel;
@property (strong) NSTextField *fromBadge;
@property (strong) NSTextField *toBadge;
@property int currentCategory;
@end
@implementation AppDelegate
- (void)applicationDidFinishLaunching:(NSNotification *)note {
 self.currentCategory = 0;
 // ── Window (580 x 600, centred) ───────────────────────────
 NSRect frame = NSMakeRect(260, 180, 580, 600);
 self.window = [[NSWindow alloc]
 initWithContentRect:frame
 styleMask:NSWindowStyleMaskTitled |
 NSWindowStyleMaskClosable |
 NSWindowStyleMaskMiniaturizable
 backing:NSBackingStoreBuffered defer:NO];
 self.window.title = @"Physics Unit Converter";
 self.window.backgroundColor = [NSColor colorWithCalibratedRed:0.09 green:0.09 blue:0.13 a [self.window center];
 NSView *v = self.window.contentView;
 // ── Header ────────────────────────────────────────────────
 NSTextField *title = [NSTextField labelWithString:@"Physics Unit Converter"];
 title.frame = NSMakeRect(20, 555, 540, 34);
 title.font = [NSFont boldSystemFontOfSize:24];
 title.textColor = [NSColor colorWithCalibratedRed:0.40 green:0.82 blue:1.0 alpha:1.0];
 [v addSubview:title];
 NSTextField *sub = [NSTextField labelWithString:
 @"SI (metric) | Imperial (US/UK) | CGS | Natural / Planck"];
 sub.frame = NSMakeRect(22, 532, 540, 18);
 sub.font = [NSFont systemFontOfSize:11];
 sub.textColor = [NSColor colorWithCalibratedWhite:0.50 alpha:1.0];
 [v addSubview:sub];
 // Legend row
 [self addColorLegendTo:v atY:510];
 NSBox *sep = [[NSBox alloc] initWithFrame:NSMakeRect(20, 500, 540, 1)];
 sep.boxType = NSBoxSeparator;
 [v addSubview:sep];
 // ── Category ──────────────────────────────────────────────
 [self addLabel:@"CATEGORY" at:NSMakeRect(20, 474, 200, 18) to:v];
 self.categoryPop = [[NSPopUpButton alloc]
 initWithFrame:NSMakeRect(20, 446, 540, 28) pullsDown:NO];
 for (int i = 0; i < CAT_COUNT; i++)
 [self.categoryPop addItemWithTitle:
 [NSString stringWithUTF8String:categoryNames[i]]];
 self.categoryPop.font = [NSFont systemFontOfSize:13];
 [self.categoryPop setTarget:self];
 [self.categoryPop setAction:@selector(categoryChanged:)];
 [v addSubview:self.categoryPop];
 // ── FROM ──────────────────────────────────────────────────
 [self addLabel:@"FROM UNIT" at:NSMakeRect(20, 416, 260, 18) to:v];
 self.fromPop = [[NSPopUpButton alloc]
 initWithFrame:NSMakeRect(20, 388, 255, 28) pullsDown:NO];
 self.fromPop.font = [NSFont systemFontOfSize:11];
 [self.fromPop setTarget:self];
 [self.fromPop setAction:@selector(unitChanged:)];
 [v addSubview:self.fromPop];
 self.fromBadge = [self makeBadge:@"" at:NSMakeRect(20, 366, 255, 18)];
 [v addSubview:self.fromBadge];
 // Arrow
 NSTextField *arrow = [NSTextField labelWithString:@"==>"];
 arrow.frame = NSMakeRect(283, 388, 40, 28);
 arrow.font = [NSFont boldSystemFontOfSize:16];
 arrow.textColor = [NSColor colorWithCalibratedRed:0.40 green:0.82 blue:1.0 alpha:1.0];
 arrow.alignment = NSTextAlignmentCenter;
 [v addSubview:arrow];
 // ── TO ────────────────────────────────────────────────────
 [self addLabel:@"TO UNIT" at:NSMakeRect(328, 416, 240, 18) to:v];
 self.toPop = [[NSPopUpButton alloc]
 initWithFrame:NSMakeRect(328, 388, 232, 28) pullsDown:NO];
 self.toPop.font = [NSFont systemFontOfSize:11];
 [self.toPop setTarget:self];
 [self.toPop setAction:@selector(unitChanged:)];
 [v addSubview:self.toPop];
 self.toBadge = [self makeBadge:@"" at:NSMakeRect(328, 366, 232, 18)];
 [v addSubview:self.toBadge];
 // ── Input ─────────────────────────────────────────────────
 [self addLabel:@"INPUT VALUE" at:NSMakeRect(20, 338, 200, 18) to:v];
 self.inputField = [[NSTextField alloc] initWithFrame:NSMakeRect(20, 310, 540, 28)];
 self.inputField.placeholderString = @"Enter a numeric value and press Enter…";
 self.inputField.font = [NSFont monospacedDigitSystemFontOfSize:14 weight:NSFontWeightRegu self.inputField.backgroundColor = [NSColor colorWithCalibratedRed:0.14 green:0.14 blue:0. self.inputField.textColor = [NSColor whiteColor];
 self.inputField.bezelStyle = NSTextFieldSquareBezel;
 [self.inputField setTarget:self];
 [self.inputField setAction:@selector(convertAction:)];
 [v addSubview:self.inputField];
 // ── Convert button ────────────────────────────────────────
 NSButton *btn = [[NSButton alloc] initWithFrame:NSMakeRect(20, 268, 540, 34)];
 btn.title = @"Convert";
 btn.bezelStyle = NSBezelStyleRounded;
 btn.font = [NSFont boldSystemFontOfSize:14];
 [btn setTarget:self];
 [btn setAction:@selector(convertAction:)];
 [v addSubview:btn];
 // ── Result ────────────────────────────────────────────────
 [self addLabel:@"RESULT" at:NSMakeRect(20, 238, 200, 18) to:v];
 self.resultField = [[NSTextField alloc] initWithFrame:NSMakeRect(20, 196, 540, 40)];
 self.resultField.editable = NO;
 self.resultField.selectable = YES;
 self.resultField.font = [NSFont monospacedDigitSystemFontOfSize:16 weight:NSFontWeightBol self.resultField.backgroundColor = [NSColor colorWithCalibratedRed:0.06 green:0.20 blue:0 self.resultField.textColor = [NSColor colorWithCalibratedRed:0.28 green:0.95 blue:0.62 al self.resultField.bezeled = YES;
 self.resultField.bezelStyle = NSTextFieldSquareBezel;
 [v addSubview:self.resultField];
 // Conversion factor
 self.formulaLabel = [NSTextField labelWithString:@""];
 self.formulaLabel.frame = NSMakeRect(20, 166, 540, 28);
 self.formulaLabel.font = [NSFont systemFontOfSize:10];
 self.formulaLabel.textColor = [NSColor colorWithCalibratedWhite:0.50 alpha:1.0];
 self.formulaLabel.alignment = NSTextAlignmentCenter;
 [v addSubview:self.formulaLabel];
 // ── Reference box ─────────────────────────────────────────
 NSBox *refBox = [[NSBox alloc] initWithFrame:NSMakeRect(20, 66, 540, 92)];
 refBox.title = @"Constants used";
 refBox.titleFont = [NSFont boldSystemFontOfSize:10];
 refBox.borderColor = [NSColor colorWithCalibratedWhite:0.22 alpha:1.0];
 refBox.fillColor = [NSColor colorWithCalibratedRed:0.11 green:0.11 blue:0.17 alpha:1.0];
 refBox.boxType = NSBoxCustom;
 [v addSubview:refBox];
 NSTextField *ref = [NSTextField labelWithString:
 @"c = 2.99792458e8 m/s | hbar = 1.054571817e-34 J.s | G = 6.67430e-11 m3/(kg. "kB = 1.380649e-23 J/K | e = 1.602176634e-19 C\n"
 "Planck: lp = 1.616255e-35 m | mp = 2.176434e-8 kg | Ep = 1.956082e9 J |  ref.frame = NSMakeRect(8, 4, 524, 68);
 ref.font = [NSFont monospacedSystemFontOfSize:9 weight:NSFontWeightRegular];
 ref.textColor = [NSColor colorWithCalibratedWhite:0.50 alpha:1.0];
 ref.cell.wraps = YES;
 [refBox addSubview:ref];
 // ── Footer ────────────────────────────────────────────────
 NSTextField *footer = [NSTextField labelWithString:
 @"Native macOS Cocoa | Apple Silicon (M1/M2/M3) optimised | clang -framework  footer.frame = NSMakeRect(20, 24, 540, 14);
 footer.font = [NSFont systemFontOfSize:9];
 footer.textColor = [NSColor colorWithCalibratedWhite:0.28 alpha:1.0];
 footer.alignment = NSTextAlignmentCenter;
 [v addSubview:footer];
 [self reloadUnitMenus];
 [self.window makeKeyAndOrderFront:nil];
}
// ─────────────────────────────────────────────────────────────
// UI helpers
// ─────────────────────────────────────────────────────────────
- (void)addColorLegendTo:(NSView *)v atY:(CGFloat)y {
 // Draw four coloured squares + labels in a row
 struct { NSString *label; NSString *conv; CGFloat x; } items[] = {
 {@"SI (metric)", @"SI", 22},
 {@"Imperial", @"Imperial", 160},
 {@"CGS", @"CGS", 298},
 {@"Natural / Planck", @"Natural", 366},
 };
 for (int i = 0; i < 4; i++) {
 NSTextField *lbl = [NSTextField labelWithString:
 [NSString stringWithFormat:@"[%@] %@", items[i].conv, items[i].label]];
 lbl.frame = NSMakeRect(items[i].x, y, 135, 16);
 lbl.font = [NSFont boldSystemFontOfSize:10];
 lbl.textColor = conventionColor(items[i].conv);
 [v addSubview:lbl];
 }
}
- (void)addLabel:(NSString *)text at:(NSRect)r to:(NSView *)parent {
 NSTextField *lbl = [NSTextField labelWithString:text];
 lbl.frame = r;
 lbl.font = [NSFont boldSystemFontOfSize:10];
 lbl.textColor = [NSColor colorWithCalibratedWhite:0.42 alpha:1.0];
 [parent addSubview:lbl];
}
- (NSTextField *)makeBadge:(NSString *)text at:(NSRect)r {
 NSTextField *b = [NSTextField labelWithString:text];
 b.frame = r;
 b.font = [NSFont boldSystemFontOfSize:10];
 b.textColor = [NSColor whiteColor];
 return b;
}
- (void)updateBadgeFor:(NSTextField *)badge cat:(int)cat idx:(int)idx {
 NSString *conv = [NSString stringWithUTF8String:unitConvention(cat, idx)];
 badge.stringValue = [NSString stringWithFormat:@"Convention: %@", conv];
 badge.textColor = conventionColor(conv);
}
// ─────────────────────────────────────────────────────────────
// Data reload
// ─────────────────────────────────────────────────────────────
- (void)reloadUnitMenus {
 [self.fromPop removeAllItems];
 [self.toPop removeAllItems];
 int n = unitCount(self.currentCategory);
 for (int i = 0; i < n; i++) {
 NSString *conv = [NSString stringWithUTF8String:unitConvention(self.currentCategory,  NSString *name = [NSString stringWithUTF8String:unitName(self.currentCategory, i)];
 NSString *entry = [NSString stringWithFormat:@"[%@] %@", conv, name];
 [self.fromPop addItemWithTitle:entry];
 [self.toPop addItemWithTitle:entry];
 }
 if (n > 1) [self.toPop selectItemAtIndex:1];
 [self updateBadgeFor:self.fromBadge cat:self.currentCategory idx:0];
 [self updateBadgeFor:self.toBadge cat:self.currentCategory idx:(n>1?1:0)];
 self.resultField.stringValue = @"";
 self.formulaLabel.stringValue = @"";
}
// ─────────────────────────────────────────────────────────────
// Actions
// ─────────────────────────────────────────────────────────────
- (void)categoryChanged:(id)sender {
 self.currentCategory = (int)self.categoryPop.indexOfSelectedItem;
 [self reloadUnitMenus];
}
- (void)unitChanged:(id)sender {
 int fi = (int)self.fromPop.indexOfSelectedItem;
 int ti = (int)self.toPop.indexOfSelectedItem;
 [self updateBadgeFor:self.fromBadge cat:self.currentCategory idx:fi];
 [self updateBadgeFor:self.toBadge cat:self.currentCategory idx:ti];
 if (self.inputField.stringValue.length > 0) [self convertAction:nil];
}
- (void)convertAction:(id)sender {
 if (self.inputField.stringValue.length == 0) {
 self.resultField.stringValue = @"";
 self.formulaLabel.stringValue = @"";
 return;
 }
 double val = self.inputField.doubleValue;
 int cat = self.currentCategory;
 int fromIdx = (int)self.fromPop.indexOfSelectedItem;
 int toIdx = (int)self.toPop.indexOfSelectedItem;
 double result = doConvert(cat, fromIdx, toIdx, val);
 // Smart formatting
 NSString *fmt;
 double absRes = fabs(result);
 if (val == 0.0) {
 fmt = @"0";
 } else if (absRes >= 1e15 || (absRes < 1e-9 && absRes > 0)) {
 fmt = [NSString stringWithFormat:@"%.8e", result];
 } else {
 fmt = [NSString stringWithFormat:@"%.10g", result];
 }
 NSString *fromName = [NSString stringWithUTF8String:unitName(cat, fromIdx)];
 NSString *toName = [NSString stringWithUTF8String:unitName(cat, toIdx)];
 self.resultField.stringValue = [NSString stringWithFormat:
 @"%g %@ = %@ %@", val, fromName, fmt, toName];
 // Factor line
 if (cat != CAT_TEMPERATURE) {
 double factor = unitTables[cat][fromIdx].toSI / unitTables[cat][toIdx].toSI;
 NSString *fromConv = [NSString stringWithUTF8String:unitConvention(cat, fromIdx)];
 NSString *toConv = [NSString stringWithUTF8String:unitConvention(cat, toIdx)];
 self.formulaLabel.stringValue = [NSString stringWithFormat:
 @"Factor: 1 %@ [%@] = %.8g %@ [%@]",
 fromName, fromConv, factor, toName, toConv];
 } else {
 self.formulaLabel.stringValue =
 @"Temperature uses non-linear (offset) conversion — no single multiplicative fact }
}
- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)app {
 return YES;
}
@end
// ─────────────────────────────────────────────────────────────
// main
// ─────────────────────────────────────────────────────────────
int main(int argc, const char *argv[]) {
 @autoreleasepool {
 NSApplication *app = [NSApplication sharedApplication];
 app.activationPolicy = NSApplicationActivationPolicyRegular;
 AppDelegate *delegate = [[AppDelegate alloc] init];
 app.delegate = delegate;
 [app activateIgnoringOtherApps:YES];
 [app run];
 }
 return 0;
}

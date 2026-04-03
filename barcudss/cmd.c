/*
 * ╔══════════════════════════════════════════════════════════════╗
 *   BARCUDSS BOARDS by Supracodelabs
 *   Advanced Emulated Terminal Interface — v1.0
 *   Colors: #004AAD | #320D53 | #76D4D5
 * ╚══════════════════════════════════════════════════════════════╝
 *
 * Compile:  gcc barcudss.c -o barcudss -lncurses
 * Run:      ./barcudss
 */

#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <signal.h>

/* ── Color pair IDs ─────────────────────────────────────────── */
#define CP_TITLE 1       /* Cyan on deep-purple              */
#define CP_BORDER 2      /* Blue on black                    */
#define CP_DIAMOND 3     /* Bright-yellow on black           */
#define CP_ICE 4         /* Cyan on black                    */
#define CP_NEON_1 5      /* Bright-cyan on black             */
#define CP_NEON_2 6      /* Bright-blue on black             */
#define CP_NEON_3 7      /* Bright-magenta on black          */
#define CP_NEON_4 8      /* Bright-green on black            */
#define CP_NEON_5 9      /* Bright-yellow on black           */
#define CP_NEON_6 10     /* Bright-red on black              */
#define CP_OPTION 11     /* White on black                   */
#define CP_OPTION_SEL 12 /* Black on cyan (selected)         */
#define CP_SUBTITLE 13   /* Blue on black                    */
#define CP_DIM 14        /* Dark grey on black               */
#define CP_FOOTER 15     /* Cyan-dim on black                */

/* ── Layout constants ───────────────────────────────────────── */
#define PANEL_W 66
#define PANEL_H 36

/* ── Menu items ─────────────────────────────────────────────── */
#define MENU_COUNT 3
static const char *MENU_LABELS[MENU_COUNT] = {
    "  Starting a New Screen Board  ",
    "  Accessing Leader Board       ",
    "  Barcudss Rules               ",
};

/* ── Neon cycle for flickering headline ─────────────────────── */
static const int NEON_PAIRS[] = {
    CP_NEON_1, CP_NEON_5, CP_NEON_2, CP_NEON_3,
    CP_NEON_4, CP_NEON_6, CP_NEON_1, CP_NEON_2};
#define NEON_COUNT 8

/* ── Globals ────────────────────────────────────────────────── */
static int selected = 0;
static int flicker_t = 0;
static int blink_on = 1;
static WINDOW *panel = NULL;

/* ─────────────────────────────────────────────────────────────
   Helper: center a string inside a given width
   ───────────────────────────────────────────────────────────── */
static int center_x(int panel_width, int str_len)
{
    int x = (panel_width - str_len) / 2;
    return x < 0 ? 0 : x;
}

/* ─────────────────────────────────────────────────────────────
   Draw the decorative double-line border of the panel
   ───────────────────────────────────────────────────────────── */
static void draw_border(WINDOW *w, int h, int ww)
{
    wattron(w, COLOR_PAIR(CP_BORDER) | A_BOLD);

    /* top bar */
    mvwaddch(w, 0, 0, ACS_ULCORNER);
    mvwaddch(w, 0, ww - 1, ACS_URCORNER);
    for (int x = 1; x < ww - 1; x++)
        mvwaddch(w, 0, x, ACS_HLINE);

    /* bottom bar */
    mvwaddch(w, h - 1, 0, ACS_LLCORNER);
    mvwaddch(w, h - 1, ww - 1, ACS_LRCORNER);
    for (int x = 1; x < ww - 1; x++)
        mvwaddch(w, h - 1, x, ACS_HLINE);

    /* sides */
    for (int y = 1; y < h - 1; y++)
    {
        mvwaddch(w, y, 0, ACS_VLINE);
        mvwaddch(w, y, ww - 1, ACS_VLINE);
    }
    wattroff(w, COLOR_PAIR(CP_BORDER) | A_BOLD);
}

/* ─────────────────────────────────────────────────────────────
   Draw a thin separator line inside the panel
   ───────────────────────────────────────────────────────────── */
static void draw_separator(WINDOW *w, int y, int ww)
{
    wattron(w, COLOR_PAIR(CP_BORDER));
    mvwaddch(w, y, 0, ACS_LTEE);
    mvwaddch(w, y, ww - 1, ACS_RTEE);
    for (int x = 1; x < ww - 1; x++)
        mvwaddch(w, y, x, ACS_HLINE);
    wattroff(w, COLOR_PAIR(CP_BORDER));
}

/* ─────────────────────────────────────────────────────────────
   Diamond + ice-cube ASCII art header icon
   ───────────────────────────────────────────────────────────── */
static void draw_icon(WINDOW *w, int start_y, int ww)
{

    /* ── Ice cube outline (7 wide × 5 tall, centered) ───────── */
    const char *ice[] = {
        " .------. ",
        " |      | ",
        " |      | ",
        " |      | ",
        " '------' ",
    };
    int ice_w = (int)strlen(ice[0]);
    int ix = center_x(ww, ice_w);

    wattron(w, COLOR_PAIR(CP_ICE) | A_DIM);
    for (int i = 0; i < 5; i++)
        mvwprintw(w, start_y + i, ix, "%s", ice[i]);
    wattroff(w, COLOR_PAIR(CP_ICE) | A_DIM);

    /* ── Diamond (◆) centred inside the cube ────────────────── */
    const char *diamond[] = {
        "  /\\  ",
        " /  \\ ",
        " \\  / ",
        "  \\/  ",
    };
    int dw = (int)strlen(diamond[0]);
    int dx = center_x(ww, dw);

    /* sparkles around diamond */
    wattron(w, COLOR_PAIR(CP_DIAMOND) | A_BOLD | A_BLINK);
    mvwprintw(w, start_y, dx - 1, "*");
    mvwprintw(w, start_y + 3, dx + dw, "*");
    wattroff(w, COLOR_PAIR(CP_DIAMOND) | A_BOLD | A_BLINK);

    /* diamond body */
    wattron(w, COLOR_PAIR(CP_NEON_1) | A_BOLD);
    for (int i = 0; i < 4; i++)
        mvwprintw(w, start_y + i, dx, "%s", diamond[i]);
    wattroff(w, COLOR_PAIR(CP_NEON_1) | A_BOLD);

    /* shining sparkle at tip */
    wattron(w, COLOR_PAIR(CP_DIAMOND) | A_BOLD | A_BLINK);
    mvwprintw(w, start_y - 1, center_x(ww, 1), "*");
    wattroff(w, COLOR_PAIR(CP_DIAMOND) | A_BOLD | A_BLINK);
}

/* ─────────────────────────────────────────────────────────────
   Application title bar
   ───────────────────────────────────────────────────────────── */
static void draw_title(WINDOW *w, int y, int ww)
{
    const char *line1 = "B A R C U D S S   B O A R D S";
    const char *line2 = "by  S u p r a c o d e l a b s";

    wattron(w, COLOR_PAIR(CP_TITLE) | A_BOLD);
    mvwprintw(w, y, center_x(ww, strlen(line1)), "%s", line1);
    wattroff(w, COLOR_PAIR(CP_TITLE) | A_BOLD);

    wattron(w, COLOR_PAIR(CP_SUBTITLE));
    mvwprintw(w, y + 1, center_x(ww, strlen(line2)), "%s", line2);
    wattroff(w, COLOR_PAIR(CP_SUBTITLE));
}

/* ─────────────────────────────────────────────────────────────
   Flickering neon headline (option 0)
   ───────────────────────────────────────────────────────────── */
static void draw_headline(WINDOW *w, int y, int ww)
{
    const char *label = MENU_LABELS[0];
    int lw = (int)strlen(label);
    int x = center_x(ww, lw + 4);

    int neon_pair = NEON_PAIRS[flicker_t % NEON_COUNT];
    int is_sel = (selected == 0);

    attr_t attrs = A_BOLD;
    if (blink_on)
        attrs |= A_STANDOUT;

    if (is_sel)
    {
        wattron(w, COLOR_PAIR(CP_OPTION_SEL) | A_BOLD | A_REVERSE);
        mvwprintw(w, y, x, "[ %s ]", label);
        wattroff(w, COLOR_PAIR(CP_OPTION_SEL) | A_BOLD | A_REVERSE);
    }
    else
    {
        wattron(w, COLOR_PAIR(neon_pair) | attrs);
        mvwprintw(w, y, x, "[ %s ]", label);
        wattroff(w, COLOR_PAIR(neon_pair) | attrs);
    }

    /* decorative size indicator */
    wattron(w, COLOR_PAIR(CP_DIM));
    mvwprintw(w, y + 1, center_x(ww, 3), "───");
    wattroff(w, COLOR_PAIR(CP_DIM));
}

/* ─────────────────────────────────────────────────────────────
   Sub-options (items 1 and 2) — smaller visual weight
   ───────────────────────────────────────────────────────────── */
static void draw_suboption(WINDOW *w, int y, int idx, int ww)
{
    const char *label = MENU_LABELS[idx];
    int lw = (int)strlen(label);
    int x = center_x(ww, lw + 6);
    int sel = (selected == idx);

    if (sel)
    {
        wattron(w, COLOR_PAIR(CP_OPTION_SEL) | A_BOLD);
        mvwprintw(w, y, x, "»  %s  «", label);
        wattroff(w, COLOR_PAIR(CP_OPTION_SEL) | A_BOLD);
    }
    else
    {
        wattron(w, COLOR_PAIR(CP_OPTION) | A_DIM);
        mvwprintw(w, y, x, "   %s   ", label);
        wattroff(w, COLOR_PAIR(CP_OPTION) | A_DIM);
    }
}

/* ─────────────────────────────────────────────────────────────
   Footer hint bar
   ───────────────────────────────────────────────────────────── */
static void draw_footer(WINDOW *w, int y, int ww)
{
    const char *hint = "↑ ↓ Navigate     ENTER Select     Q Quit";
    wattron(w, COLOR_PAIR(CP_FOOTER) | A_DIM);
    mvwprintw(w, y, center_x(ww, strlen(hint)), "%s", hint);
    wattroff(w, COLOR_PAIR(CP_FOOTER) | A_DIM);
}

/* ─────────────────────────────────────────────────────────────
   Render the full main-menu screen
   ───────────────────────────────────────────────────────────── */
static void render_menu(void)
{
    werase(panel);
    draw_border(panel, PANEL_H, PANEL_W);

    /* title */
    draw_title(panel, 2, PANEL_W);

    draw_separator(panel, 5, PANEL_W);

    /* icon (ice cube y=7, needs 1 sparkle row above → y=7 gives room) */
    draw_icon(panel, 7, PANEL_W);

    draw_separator(panel, 13, PANEL_W);

    /* headline — flickering large option */
    draw_headline(panel, 16, PANEL_W);

    draw_separator(panel, 19, PANEL_W);

    /* sub-options */
    draw_suboption(panel, 22, 1, PANEL_W);
    draw_suboption(panel, 25, 2, PANEL_W);

    draw_separator(panel, PANEL_H - 4, PANEL_W);
    draw_footer(panel, PANEL_H - 3, PANEL_W);

    wrefresh(panel);
}

/* ─────────────────────────────────────────────────────────────
   Action screen shown after ENTER
   ───────────────────────────────────────────────────────────── */
static void show_action_screen(int choice)
{
    const char *titles[] = {
        "STARTING A NEW SCREEN BOARD",
        "LEADER BOARD",
        "BARCUDSS RULES",
    };
    const char *msgs[] = {
        "Initialising a fresh board...",
        "Loading rankings...",
        "Loading the rules of the game...",
    };

    werase(panel);
    draw_border(panel, PANEL_H, PANEL_W);

    wattron(panel, COLOR_PAIR(CP_TITLE) | A_BOLD);
    mvwprintw(panel, 4, center_x(PANEL_W, strlen(titles[choice])),
              "%s", titles[choice]);
    wattroff(panel, COLOR_PAIR(CP_TITLE) | A_BOLD);

    draw_separator(panel, 6, PANEL_W);

    wattron(panel, COLOR_PAIR(CP_ICE) | A_DIM);
    mvwprintw(panel, 10, center_x(PANEL_W, strlen(msgs[choice])),
              "%s", msgs[choice]);
    wattroff(panel, COLOR_PAIR(CP_ICE) | A_DIM);

    /* animated dots */
    wrefresh(panel);
    for (int d = 0; d < 5; d++)
    {
        wattron(panel, COLOR_PAIR(CP_NEON_1) | A_BOLD);
        mvwprintw(panel, 12, center_x(PANEL_W, 3 + d), "%.*s",
                  d + 1, "•••••");
        wattroff(panel, COLOR_PAIR(CP_NEON_1) | A_BOLD);
        wrefresh(panel);
        usleep(220000);
    }

    wattron(panel, COLOR_PAIR(CP_NEON_4) | A_BOLD);
    const char *back = "[ Press any key to return ]";
    mvwprintw(panel, PANEL_H - 5, center_x(PANEL_W, strlen(back)), "%s", back);
    wattroff(panel, COLOR_PAIR(CP_NEON_4) | A_BOLD);

    wrefresh(panel);
    nodelay(panel, FALSE);
    wgetch(panel);
    nodelay(panel, TRUE);
}

/* ─────────────────────────────────────────────────────────────
   Initialise ncurses + colour pairs
   ───────────────────────────────────────────────────────────── */
static void init_colors(void)
{
    start_color();
    use_default_colors();

    /* Approximate the brand palette with the 256-color xterm cube   */
    /* #004AAD ≈ colour 26  (0,0,175 → close to 004AAD)              */
    /* #320D53 ≈ colour 53  (95,0,95 → closest deep purple)          */
    /* #76D4D5 ≈ colour 116 (95,215,215 → close to 76D4D5)           */

    init_pair(CP_TITLE, 116, 53);      /* cyan-teal on deep purple */
    init_pair(CP_BORDER, 26, -1);      /* brand blue on default    */
    init_pair(CP_DIAMOND, 226, -1);    /* bright yellow            */
    init_pair(CP_ICE, 116, -1);        /* teal                     */
    init_pair(CP_NEON_1, 51, -1);      /* bright cyan              */
    init_pair(CP_NEON_2, 27, -1);      /* vivid blue               */
    init_pair(CP_NEON_3, 201, -1);     /* bright magenta           */
    init_pair(CP_NEON_4, 82, -1);      /* neon green               */
    init_pair(CP_NEON_5, 226, -1);     /* bright yellow            */
    init_pair(CP_NEON_6, 196, -1);     /* bright red               */
    init_pair(CP_OPTION, 255, -1);     /* near-white               */
    init_pair(CP_OPTION_SEL, -1, 116); /* default on teal          */
    init_pair(CP_SUBTITLE, 26, -1);    /* brand blue               */
    init_pair(CP_DIM, 59, -1);         /* dim grey                 */
    init_pair(CP_FOOTER, 116, -1);     /* teal dim                 */
}

/* ─────────────────────────────────────────────────────────────
   Main entry point
   ───────────────────────────────────────────────────────────── */
int main(void)
{
    /* ncurses bootstrap */
    initscr();
    cbreak();
    noecho();
    curs_set(0);
    keypad(stdscr, TRUE);

    if (!has_colors())
    {
        endwin();
        fprintf(stderr, "Your terminal does not support colours.\n");
        return 1;
    }

    init_colors();

    /* Position panel centred on screen */
    int scr_h, scr_w;
    getmaxyx(stdscr, scr_h, scr_w);
    int panel_y = (scr_h - PANEL_H) / 2;
    int panel_x = (scr_w - PANEL_W) / 2;
    if (panel_y < 0)
        panel_y = 0;
    if (panel_x < 0)
        panel_x = 0;

    panel = newwin(PANEL_H, PANEL_W, panel_y, panel_x);
    if (!panel)
    {
        endwin();
        return 1;
    }

    /* Background fill */
    wbkgd(stdscr, COLOR_PAIR(CP_BORDER));
    wbkgd(panel, COLOR_PAIR(CP_TITLE));
    refresh();

    nodelay(panel, TRUE); /* non-blocking getch */

    /* ── Main event loop ──────────────────────────────────── */
    int running = 1;
    int tick = 0;

    while (running)
    {
        /* Update flicker state every 6 ticks (~120 ms) */
        tick++;
        if (tick % 6 == 0)
        {
            flicker_t++;
            blink_on = !blink_on;
        }

        render_menu();
        usleep(20000); /* ~50 fps */

        int ch = wgetch(panel);
        switch (ch)
        {
        case KEY_UP:
            selected = (selected - 1 + MENU_COUNT) % MENU_COUNT;
            break;
        case KEY_DOWN:
            selected = (selected + 1) % MENU_COUNT;
            break;
        case '\n':
        case KEY_ENTER:
            nodelay(panel, FALSE);
            show_action_screen(selected);
            nodelay(panel, TRUE);
            break;
        case 'q':
        case 'Q':
            running = 0;
            break;
        default:
            break;
        }
    }

    /* Goodbye screen */
    werase(panel);
    draw_border(panel, PANEL_H, PANEL_W);
    const char *bye = "See you on the boards!";
    wattron(panel, COLOR_PAIR(CP_NEON_1) | A_BOLD);
    mvwprintw(panel, PANEL_H / 2, center_x(PANEL_W, strlen(bye)), "%s", bye);
    wattroff(panel, COLOR_PAIR(CP_NEON_1) | A_BOLD);
    wrefresh(panel);
    usleep(1200000);

    delwin(panel);
    endwin();
    return 0;
}

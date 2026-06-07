"""
End-to-end test for 영어 빙고.

Tests:
  T1 — page loads, board renders with sample words (5x5)
  T2 — switch to 4x4, board rerenders with 16 cells
  T3 — fill simple row & verify BINGO line detected (1 line)
  T4 — caller: next word increments counter, shows word
  T5 — repeat call works (no error)
  T6 — reset clears called counter
  T7 — print section is built when print is triggered (DOM-only check)
  T8 — no JS console errors during full flow
"""
import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect, ConsoleMessage

URL = os.environ.get("APP_URL", "http://127.0.0.1:5180/")
ART = Path(__file__).parent / "artifacts"
ART.mkdir(exist_ok=True)


def main():
    errors = []
    warnings = []
    passed = []
    failed = []

    def record(name, ok, detail=""):
        (passed if ok else failed).append((name, detail))
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {name}{(' — ' + detail) if detail else ''}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        # Auto-accept dialogs (confirm on reset)
        page = context.new_page()
        page.on("dialog", lambda d: d.accept())

        def on_console(msg: ConsoleMessage):
            text = msg.text
            if msg.type == "error":
                # Filter known noise: TTS rejection ("not-allowed") sometimes shows
                if "speechSynthesis" in text or "not-allowed" in text:
                    warnings.append(text)
                else:
                    errors.append(f"console.error: {text}")
            elif msg.type == "warning":
                warnings.append(text)

        page.on("console", on_console)
        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))

        # ---- T1 ----
        page.goto(URL)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(ART / "01_home.png"), full_page=True)
        cells = page.locator(".board .cell")
        cell_count = cells.count()
        record("T1 home loads, 5x5 board = 25 cells",
               cell_count == 25, f"got {cell_count}")

        # ---- T2 ----
        page.locator("#size-4").click()
        page.wait_for_timeout(150)
        cell_count = page.locator(".board .cell").count()
        record("T2 switch to 4x4 = 16 cells", cell_count == 16, f"got {cell_count}")
        page.screenshot(path=str(ART / "02_4x4.png"), full_page=True)

        # back to 5x5 for bingo test
        page.locator("#size-5").click()
        page.wait_for_timeout(150)
        cell_count = page.locator(".board .cell").count()
        record("T2b switch back to 5x5 = 25 cells", cell_count == 25, f"got {cell_count}")

        # ---- T3 ----
        # Click first row 0..4 → expect bingo count = 1
        for i in range(5):
            page.locator(f'.board .cell[data-idx="{i}"]').click()
        page.wait_for_timeout(200)
        bingo_text = page.locator("#bingo-count").inner_text().strip()
        in_bingo_cnt = page.locator(".cell.in-bingo").count()
        record("T3 row 0 marked → bingo count = 1",
               bingo_text == "1", f"bingo-count='{bingo_text}'")
        record("T3b in-bingo cells = 5",
               in_bingo_cnt == 5, f"got {in_bingo_cnt}")
        page.screenshot(path=str(ART / "03_bingo.png"), full_page=True)

        # ---- T4 ----
        # Click next button → counter goes 0 → 1
        page.locator("#next-btn").click()
        page.wait_for_timeout(250)
        called_text = page.locator("#called-count").inner_text().strip()
        active_visible = page.locator("#caller-active").is_visible()
        word_text = page.locator("#caller-word").inner_text().strip()
        record("T4 next → called-count = 1",
               called_text == "1", f"got '{called_text}'")
        record("T4b caller active visible", active_visible)
        record("T4c caller-word non-empty", len(word_text) > 0, f"word='{word_text}'")
        page.screenshot(path=str(ART / "04_caller.png"), full_page=True)

        # ---- T5 ----
        # repeat — should still show same word; should not throw
        page.locator("#repeat-btn").click()
        page.wait_for_timeout(150)
        word_text2 = page.locator("#caller-word").inner_text().strip()
        record("T5 repeat keeps same word", word_text == word_text2,
               f"before='{word_text}' after='{word_text2}'")

        # Call 3 more words
        for _ in range(3):
            page.locator("#next-btn").click()
            page.wait_for_timeout(120)
        called_text = page.locator("#called-count").inner_text().strip()
        record("T5b after 4 total nexts called-count = 4",
               called_text == "4", f"got '{called_text}'")

        # ---- T6 ----
        page.locator("#reset-btn").click()
        page.wait_for_timeout(200)
        called_text = page.locator("#called-count").inner_text().strip()
        empty_visible = page.locator("#caller-empty").is_visible()
        record("T6 reset → called-count = 0", called_text == "0", f"got '{called_text}'")
        record("T6b reset → caller-empty visible", empty_visible)

        # ---- T7 ----
        # Mock window.print so it doesn't open dialog
        page.evaluate("window.print = () => { window.__printed = true; };")
        page.locator("#print-btn").click()
        page.wait_for_timeout(200)
        print_count = page.locator("#print-section .print-page").count()
        printed_called = page.evaluate("window.__printed === true")
        record("T7 print builds 2 boards", print_count == 2, f"got {print_count}")
        record("T7b window.print() called", printed_called)

        # ---- T8 ----
        record("T8 no JS console errors",
               len(errors) == 0,
               f"errors={errors[:3]}")

        # Final screenshots
        page.screenshot(path=str(ART / "final_5x5.png"), full_page=True)

        # 4x4 final shot
        page.locator("#size-4").click()
        page.wait_for_timeout(150)
        page.screenshot(path=str(ART / "final_4x4.png"), full_page=True)

        browser.close()

    print("\n--- Summary ---")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    if warnings:
        print(f"Warnings (filtered): {len(warnings)}")
    if errors:
        print("Console errors:")
        for e in errors[:5]:
            print(" ·", e)
    if failed:
        print("Failures:")
        for n, d in failed:
            print(f" · {n} {d}")
        sys.exit(1)
    print("All tests green.")


if __name__ == "__main__":
    main()

"""
Genera ficha.pdf a partir de ficha.html usando Playwright + Chromium.
Uso: python gen_pdf.py
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def main():
    base = Path(__file__).parent.resolve()
    html_path = base / "ficha.html"
    pdf_path  = base / "ficha.pdf"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(html_path.as_uri(), wait_until="networkidle")

        await page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        await browser.close()

    print(f"PDF generado: {pdf_path}")


asyncio.run(main())

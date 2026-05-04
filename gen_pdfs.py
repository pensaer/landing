"""
Convierte todos los ficha.html en ficha.pdf usando Playwright + Chromium.
Uso: python gen_pdfs.py
Requiere: pip install playwright && playwright install chromium
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(r"C:\Users\marcelo\Documents\Landings")


async def main():
    ficha_files = sorted(BASE.glob("*/ficha.html"))
    print(f"Encontradas {len(ficha_files)} fichas HTML...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for ficha_html in ficha_files:
            pdf_path = ficha_html.with_suffix(".pdf")
            page = await browser.new_page()
            await page.goto(ficha_html.as_uri(), wait_until="networkidle")
            await page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            await page.close()
            print(f"  PDF: {ficha_html.parent.name}/ficha.pdf")

        await browser.close()

    print(f"\nTotal: {len(ficha_files)} PDFs generados.")


asyncio.run(main())

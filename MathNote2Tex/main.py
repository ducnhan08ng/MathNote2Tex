import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Tải biến môi trường
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Lỗi: Chưa tìm thấy GEMINI_API_KEY trong file .env!")

client = genai.Client(api_key=API_KEY)

# System Prompt định hướng cấu trúc LaTeX chuẩn học thuật
SYSTEM_PROMPT = """
Bạn là một trợ lý học thuật chuyên nghiệp về Toán cao cấp và LaTeX.
Nhiệm vụ của bạn là chuyển đổi văn bản ghi chú Toán học thô của sinh viên thành một file mã nguồn LaTeX hoàn chỉnh, sạch đẹp, sẵn sàng để compile sang PDF.

Yêu cầu bắt buộc:
1. Sử dụng documentclass{article}, gói tiếng Việt \\usepackage[utf8]{vietnam} hoặc babel, cùng các gói toán học: amsmath, amssymb, amsthm, geometry.
2. Tự động phân loại và bọc nội dung vào các môi trường tương ứng: Định lý, Định nghĩa, Công thức (dùng align* hoặc equation*), và Bài tập (dùng itemize/enumerate).
3. Chuyển đổi các ký hiệu gõ tắt (như <=, ->, ^, ma trận [a b; c d]) sang đúng cú pháp LaTeX (\\leq, \\to, \\begin{pmatrix}...).
4. CHỈ TRẢ VỀ mã nguồn LaTeX nằm trong cặp thẻ \\documentclass đến \\end{document}, không giải thích gì thêm.
"""

def read_raw_notes(file_path: str) -> str:
    """Đọc nội dung ghi chú thô từ file text."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def clean_latex_output(raw_response: str) -> str:
    """Sử dụng Regex để lọc bỏ các dấu ```latex thừa từ phản hồi của AI."""
    cleaned = re.sub(r"^```(?:latex|tex)?\s*", "", raw_response.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()

def convert_notes_to_latex(notes_content: str) -> str:
    """Gửi request tới Gemini API để chuyển đổi ghi chú sang LaTeX."""
    print("[*] Đang kết nối Gemini API và xử lý cú pháp Toán học...")
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"Hãy chuyển đổi đoạn ghi chú sau sang LaTeX:\n\n{notes_content}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2, # Giữ temperature thấp để đảm bảo tính chính xác của công thức
        ),
    )
    return clean_latex_output(response.text)

def save_tex_file(latex_code: str, output_path: str):
    """Lưu mã nguồn LaTeX ra file .tex."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"[+] Hoàn tất! File LaTeX đã được lưu tại: {output_path}")

if __name__ == "__main__":
    INPUT_FILE = "sample_notes.txt"
    OUTPUT_FILE = "output_notes.tex"

    print("=== MATHNOTE2TEX: AI LATEX CONVERTER ===")
    try:
        raw_text = read_raw_notes(INPUT_FILE)
        print(f"[*] Đã đọc file ghi chú đầu vào ({len(raw_text)} ký tự).")
        
        latex_result = convert_notes_to_latex(raw_text)
        save_tex_file(latex_result, OUTPUT_FILE)
        
        print("[*] Bạn có thể biên dịch file output_notes.tex bằng TeXstudio, VS Code LaTeX Workshop hoặc Overleaf.")
    except Exception as e:
        print(f"[!] Đã xảy ra lỗi: {e}")
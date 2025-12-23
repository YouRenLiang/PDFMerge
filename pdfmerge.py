import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger
import os

class PDFMergeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 合併工具")
        window_width = 600
        window_height = 450
        
        # 獲取螢幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 計算置中座標
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # 設定視窗幾何形狀：寬x高+左位移+上位移
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # -----------------------
        
        self.path1 = None
        self.path2 = None

        # 標題說明
        tk.Label(root, text="請將 PDF 檔案拖入下方區塊", font=("Arial", 12)).pack(pady=10)

        # 容器框架
        frame = tk.Frame(root)
        frame.pack(expand=True, fill="both", padx=20, pady=10)

        # 左側區塊 (前者)
        self.box1 = tk.Label(frame, text="【 1. 放在前面 】\n拖曳檔案至此", 
                             bg="#e1f5fe", relief="groove", width=25)
        self.box1.pack(side="left", expand=True, fill="both", padx=5)
        self.box1.drop_target_register(DND_FILES)
        self.box1.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, 1))

        # 右側區塊 (後者)
        self.box2 = tk.Label(frame, text="【 2. 放在後面 】\n拖曳檔案至此", 
                             bg="#fff9c4", relief="groove", width=25)
        self.box2.pack(side="left", expand=True, fill="both", padx=5)
        self.box2.drop_target_register(DND_FILES)
        self.box2.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, 2))

        # 合併按鈕 (預設隱藏)
        self.merge_btn = tk.Button(root, text="開始合併檔案", command=self.merge_pdfs,
                                   bg="#4caf50", fg="white", font=("Arial", 12, "bold"), 
                                   height=2, width=20)

    def handle_drop(self, event, box_num):
        # 處理檔案路徑 (去除可能的大括號)
        file_path = event.data.strip('{}')
        
        if not file_path.lower().endswith(".pdf"):
            messagebox.showerror("錯誤", "僅支援 PDF 格式！")
            return

        file_name = os.path.basename(file_path)
        
        if box_num == 1:
            self.path1 = file_path
            self.box1.config(text=f"【 已就緒 (前) 】\n{file_name}", bg="#81d4fa")
        else:
            self.path2 = file_path
            self.box2.config(text=f"【 已就緒 (後) 】\n{file_name}", bg="#fff59d")

        # 檢查是否都有檔案，若有則顯示按鈕
        if self.path1 and self.path2:
            self.merge_btn.pack(pady=20)

    def merge_pdfs(self):
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="儲存合併後的檔案"
        )
        
        if output_path:
            try:
                merger = PdfMerger()
                merger.append(self.path1)
                merger.append(self.path2)
                merger.write(output_path)
                merger.close()
                messagebox.showinfo("成功", f"檔案已儲存至：\n{output_path}")
                # 重設狀態
                self.reset_gui()
            except Exception as e:
                messagebox.showerror("失敗", f"發生錯誤：{str(e)}")

    def reset_gui(self):
        self.path1 = self.path2 = None
        self.box1.config(text="【 1. 放在前面 】\n拖曳檔案至此", bg="#e1f5fe")
        self.box2.config(text="【 2. 放在後面 】\n拖曳檔案至此", bg="#fff9c4")
        self.merge_btn.pack_forget()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergeGUI(root)
    root.mainloop()

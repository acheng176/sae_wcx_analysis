import os
import json
from pdf_processor import process_pdfs
from ai_extractor import extract_structured_data
from categorizer import add_categories_to_data
from db_handler import DatabaseHandler
from excel_writer import write_to_excel

def save_to_json(data, year, output_dir=r"output\file"):
    """抽出したデータをJSONファイルに保存する"""
    try:
        # 出力ディレクトリの作成
        os.makedirs(output_dir, exist_ok=True)
        
        # 出力ファイル名の生成
        output_file = os.path.join(output_dir, f"sae_wcx_{year}.json")
        
        # JSONファイルに書き込み
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"JSONファイルを出力しました: {output_file}")
        return True
        
    except Exception as e:
        print(f"警告: JSONファイルの保存中にエラーが発生しました: {str(e)}")
        return False

def main(debug_mode=False, debug_chunk_count=5):
    """メイン処理を実行する
    
    Args:
        debug_mode (bool): デバッグモードの場合True
        debug_chunk_count (int): デバッグモード時に処理するチャンク数
    """
    try:
        # 入力ディレクトリの設定
        input_dir = "data/input"
        
        # PDFファイルの処理
        try:
            print("\nPDFファイルの処理を開始します...")
            pdf_texts = process_pdfs(input_dir)
            if not pdf_texts:
                print("Error: PDFファイルの処理に失敗しました")
                return
        except Exception as e:
            print(f"Error: PDFファイルの処理中にエラーが発生: {str(e)}")
            return
        
        # 年の抽出
        try:
            print("\n年の抽出を開始します...")
            year = extract_year_from_text(pdf_texts[0])
            if not year:
                print("Error: 年の抽出に失敗しました")
                return
            print(f"抽出された年: {year}")
        except Exception as e:
            print(f"Error: 年の抽出中にエラーが発生: {str(e)}")
            return
        
        # データの抽出
        try:
            print("\nデータの抽出を開始します...")
            extracted_data = extract_structured_data(pdf_texts[0], debug_mode, debug_chunk_count)
            if not extracted_data:
                print("Error: データの抽出に失敗しました")
                return
        except Exception as e:
            print(f"Error: データの抽出中にエラーが発生: {str(e)}")
            return
        
        # データの検証
        try:
            print("\nデータの検証を開始します...")
            if not validate_data_format(extracted_data):
                print("Error: データの検証に失敗しました")
                return
        except Exception as e:
            print(f"Error: データの検証中にエラーが発生: {str(e)}")
            return
        
        # カテゴリーの分類
        try:
            print("\nカテゴリーの分類を開始します...")
            categorized_data = add_categories_to_data(extracted_data)
            if not categorized_data:
                print("Error: カテゴリーの分類に失敗しました")
                return
        except Exception as e:
            print(f"Error: カテゴリーの分類中にエラーが発生: {str(e)}")
            return
        
        # データベースへの保存
        try:
            print("\nデータベースへの保存を開始します...")
            db = DatabaseHandler()
            if not db.store_data(categorized_data, year):
                print("Error: データベースへの保存に失敗しました")
                return
        except Exception as e:
            print(f"Error: データベースへの保存中にエラーが発生: {str(e)}")
            return
        
        # Excelファイルへの書き込み
        try:
            print("\nExcelファイルへの書き込みを開始します...")
            if not write_to_excel(categorized_data, year):
                print("Error: Excelファイルへの書き込みに失敗しました")
                return
        except Exception as e:
            print(f"Error: Excelファイルへの書き込み中にエラーが発生: {str(e)}")
            return
        
        print("\n処理が正常に完了しました")
        
    except Exception as e:
        print(f"Error: メイン処理中にエラーが発生: {str(e)}")

if __name__ == "__main__":
    # デバッグモードで実行する場合は、以下のように引数を指定
    # main(debug_mode=True, debug_chunk_count=5)
    
    # 通常モードで実行する場合は、引数なしで呼び出し
    main()
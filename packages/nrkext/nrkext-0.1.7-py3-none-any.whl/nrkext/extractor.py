import pandas as pd
from datetime import datetime
import os
import openpyxl


class PTRCalibration:
    TODAY = datetime.today().date()

    def __init__(self, path):
        self.file_list = list(
            map(
                lambda xcl: os.path.join(path, xcl),
                filter(
                    lambda file: os.path.splitext(file)[-1].lower()
                    in (".xlsx", ".xlsm"),
                    os.listdir(path),
                ),
            )
        )
        self.frame = pd.DataFrame()
        self.frames = []
        self.path = path
        self.permission = []

    def extract_data(self):
        for file in self.file_list:
            try:
                read = pd.read_excel(file, sheet_name=0).dropna(how="all")
                read["Log File"] = os.path.splitext(os.path.split(file)[-1])[0]
                self.frames.append(read)
            except PermissionError:
                self.permission.append(os.path.split(file)[-1].split("_")[0])

    def save(self):
        extracted_path = os.path.join(self.path, "Extracted")
        if not os.path.isdir(extracted_path):
            os.mkdir(extracted_path)
        archive_path = os.path.join(extracted_path, "Archive")
        if not os.path.isdir(archive_path):
            os.mkdir(archive_path)
        out = pd.concat(self.frames)
        try:
            if "ID" in out.columns:
                out = out.set_index("ID").sort_index().reset_index()
                try:
                    out['ID']  = out['ID'].fillna(0).apply(lambda x: pd.to_numeric(x, errors='coerce')).astype(int)
                except:
                    pass
        except:
            pass
        excel_path = os.path.join(extracted_path, f"Excel Extracted Log Files.xlsx")
        excel_archive_path = os.path.join(
            archive_path, f"Excel Extracted Log Files_{self.TODAY}.xlsx"
        )
        csv_path = os.path.join(extracted_path, f"Extracted Log Files.csv")
        csv_archive_path = os.path.join(
            archive_path, f"Extracted Log Files_{self.TODAY}.csv"
        )

        self._save(out, excel_path, csv=False)
        self._save(out, excel_archive_path, csv=False)
        self._save(out, csv_path, csv=True)
        self._save(out, csv_archive_path, csv=True)

    def _save(self, out, path, csv):
        if not csv:
            try:
                out.to_excel(path, index=False)
            except PermissionError:
                self.permission.append(path)
        else:
            try:
                out.to_csv(path, index=False)
            except PermissionError:
                self.permission.append(path)

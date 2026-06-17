import csv
import os
import subprocess
import tempfile
from pathlib import Path

import process


def find_and_diff_files():
    # Define and resolve paths
    my_dir = Path("../../mine").resolve()
    mad_dir = Path("../../madgrades").resolve()
    output_dir = Path("../../discrepancies").resolve()

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scanning directories...")

    # Step 1: Recursively find all TSV files in 'mine'
    my_files = {
        p.relative_to(my_dir): p
        for p in my_dir.rglob("*.tsv")
        if p.is_file()
    }

    # Step 2: Iterate through 'madgrades' to find matches
    for mad_path in mad_dir.rglob("*.tsv"):
        if not mad_path.is_file():
            continue

        relative_path = mad_path.relative_to(mad_dir)

        if relative_path in my_files:
            my_path = my_files[relative_path]

            print(f"\nProcessing matching file: {relative_path}")

            # Step 3: Open both TSV files for your custom processing
            with (
                open(my_path, mode="r", encoding="utf-8", newline="") as f1,
                open(mad_path, mode="r", encoding="utf-8", newline="") as f2,
            ):

                my_reader = csv.reader(f1, delimiter="\t")
                mad_reader = csv.reader(f2, delimiter="\t")

                # Your custom processing returns lists of rows
                my_rows = process.standardize_my_dir_2(list(my_reader))
                mad_rows = process.standardize_madgrades_dir_2(list(mad_reader))

                # for i in range(5, 10): print(my_rows[i]); print(mad_rows[i])

            # Step 4: Write processed data to temporary files for diffing
            # delete=True ensures the OS wipes them when closed
            with (
                tempfile.NamedTemporaryFile(
                    mode="w+", encoding="utf-8", newline="", delete=True
                ) as tmp_my,
                tempfile.NamedTemporaryFile(
                    mode="w+", encoding="utf-8", newline="", delete=True
                ) as tmp_mad,
            ):

                # Write processed rows back into temporary TSV formats
                my_writer = csv.writer(tmp_my, delimiter="\t")
                mad_writer = csv.writer(tmp_mad, delimiter="\t")

                my_writer.writerows(my_rows)
                mad_writer.writerows(mad_rows)

                # Flush internal buffers to disk so the Linux diff command can see the data
                tmp_my.flush()
                tmp_mad.flush()

                # Step 5: Run the native Linux diff command on the temp files
                # Label flags (--label) make the diff output look clean and reference original names
                result = subprocess.run(
                    [
                        "diff",
                        "-u",
                        "--label",
                        f"mine/{relative_path}",
                        "--label",
                        f"madgrades/{relative_path}",
                        tmp_my.name,
                        tmp_mad.name,
                    ],
                    capture_output=True,
                    text=True,
                )

            # Step 6: Save differences if found
            if result.returncode == 1:
                safe_filename = (
                    str(relative_path).replace(os.sep, "_") + ".diff"
                )
                output_file_path = output_dir / safe_filename

                with open(
                    output_file_path, "w", encoding="utf-8"
                ) as output_file:
                    output_file.write(result.stdout)

                print(f"❌ Differences saved to: {output_file_path}")

            elif result.returncode == 0:
                print("✅ Processed files are identical.")
            else:
                print(f"⚠️ Error running diff: {result.stderr}")


if __name__ == "__main__":
    find_and_diff_files()

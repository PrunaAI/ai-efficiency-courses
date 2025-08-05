#!/usr/bin/env python3
"""
Script to add Google Colab buttons to all Jupyter notebooks.
This script will add a Colab button at the top of each notebook that opens it in Google Colab.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ColabButtonAdder:
    """Adds Google Colab buttons to Jupyter notebooks."""

    def __init__(
        self,
        base_url: str = "https://colab.research.google.com/github/PrunaAI/ai-efficiency-courses/blob/main/",
    ):
        """
        Initialize the Colab button adder.

        Args:
            base_url: The base URL for Google Colab with the repository path
        """
        self.base_url = base_url

    def create_colab_button_cell(self, notebook_path: str) -> Dict[str, Any]:
        """
        Create a markdown cell with a Google Colab button.

        Args:
            notebook_path: Path to the notebook file

        Returns:
            Dictionary representing the markdown cell
        """
        # Convert path to GitHub-style path
        github_path = str(Path(notebook_path)).replace("\\", "/")

        colab_url = f"{self.base_url}{github_path}"

        button_html = f"""
<div align="center">
  <a href="{colab_url}" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
  </a>
</div>

---
**💡 Tip**: Click the button above to open this notebook in Google Colab for free GPU access!
        """.strip()

        return {"cell_type": "markdown", "metadata": {}, "source": [button_html]}

    def add_colab_button_to_notebook(self, notebook_path: str) -> bool:
        """
        Add a Google Colab button to a Jupyter notebook.

        Args:
            notebook_path: Path to the notebook file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Read the notebook
            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = json.load(f)

            # Check if button already exists by looking for colab-badge.svg in any markdown cell
            if notebook.get("cells"):
                for cell in notebook["cells"]:
                    if cell.get("cell_type") == "markdown" and "colab-badge.svg" in str(
                        cell.get("source", [])
                    ):
                        print(f"✅ Colab button already exists in {notebook_path}")
                        return True

            # Create the button cell
            button_cell = self.create_colab_button_cell(notebook_path)

            # Insert the button cell at the beginning
            notebook["cells"].insert(0, button_cell)

            # Write the updated notebook
            with open(notebook_path, "w", encoding="utf-8") as f:
                json.dump(notebook, f, indent=2, ensure_ascii=False)

            print(f"✅ Added Colab button to {notebook_path}")
            return True

        except Exception as e:
            print(f"❌ Error processing {notebook_path}: {e}")
            return False

    def process_directory(self, directory_path: str) -> Dict[str, int]:
        """
        Process all notebooks in a directory.

        Args:
            directory_path: Path to the directory containing notebooks

        Returns:
            Dictionary with success and failure counts
        """
        results = {"success": 0, "failed": 0}

        if not os.path.exists(directory_path):
            print(f"❌ Directory not found: {directory_path}")
            return results

        for file_path in Path(directory_path).glob("*.ipynb"):
            if self.add_colab_button_to_notebook(str(file_path)):
                results["success"] += 1
            else:
                results["failed"] += 1

        return results


def main():
    """Main function to add Colab buttons to all notebooks."""
    print("🚀 Adding Google Colab buttons to all notebooks...")

    # Initialize the adder
    adder = ColabButtonAdder()

    # Process exercises directory
    print("\n📁 Processing exercises directory...")
    exercises_results = adder.process_directory("exercises")

    # Process solutions directory
    print("\n📁 Processing solutions directory...")
    solutions_results = adder.process_directory("solutions")

    # Print summary
    print("\n📊 Summary:")
    print(
        f"Exercises: {exercises_results['success']} successful, {exercises_results['failed']} failed"
    )
    print(
        f"Solutions: {solutions_results['success']} successful, {solutions_results['failed']} failed"
    )

    total_success = exercises_results["success"] + solutions_results["success"]
    total_failed = exercises_results["failed"] + solutions_results["failed"]

    print(f"\n🎉 Total: {total_success} notebooks updated successfully!")
    if total_failed > 0:
        print(f"⚠️  {total_failed} notebooks failed to update")


if __name__ == "__main__":
    main()

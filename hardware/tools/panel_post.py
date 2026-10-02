def kikitPostprocess(panel, arg):
    for footprint in panel.board.GetFootprints():
        ref = footprint.GetReference()

        if ref.startswith("KiKit_FID_") or ref.startswith("KiKit_TO_"):
            if hasattr(footprint, "SetExcludedFromPosFiles"):
                footprint.SetExcludedFromPosFiles(True)

            if hasattr(footprint, "SetExcludedFromBOM"):
                footprint.SetExcludedFromBOM(True)

            if hasattr(footprint, "SetBoardOnly"):
                footprint.SetBoardOnly(True)
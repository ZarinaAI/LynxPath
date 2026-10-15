# 90-second OpenCareFlow live demo script

1. **Open the fracture scenario at T = 0.**
   - Patient requirement is already declared: X-ray + orthopaedics.
   - Point out that Hospital A is nearest at 8 minutes.
   - Hospital B ranks first because its operational delays are much smaller.

2. **Show inspectability.**
   - Expand Hospital B.
   - Show travel, ED delay, X-ray delay, orthopaedics delay, range, freshness and confidence.

3. **Click Next →.**
   - Hospital B ED load rises.
   - Hospital C clears imaging and orthopaedics queues.
   - The winner changes from B to C.
   - Read the generated explanation of the change.

4. **Click Next → again.**
   - Hospital C reports a temporary orthopaedics closure.
   - It becomes ineligible for this pathway.

5. **Finish on the schema.**
   - The core project is the open capacity-signal representation plus reproducible estimator and scenarios.
   - Ask contributors to review the schema, add adapters and add scenarios.

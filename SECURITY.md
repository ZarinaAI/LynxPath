# Security Policy

LynxPath v0.1 is a synthetic research/demo project and must not process real patient data.

Please do not open public issues containing credentials, vulnerabilities in a real hospital system, patient information or confidential operational data.

For the public demo repository:

- keep all scenario inputs synthetic;
- never commit secrets;
- pin or constrain dependencies;
- use the included CI before merging changes;
- treat external adapters as untrusted input boundaries.

A private security contact should be added before any deployment connected to a real healthcare environment.

# Generated Agile User Story Cards

User Story Cards for LIC Business Process Digitization & Package Creation Platform

US-01: Dynamic Policy & Rider Bundling
- Stakeholder: Customer, Agent
- FR Origin: FR-1.1.2
- As a customer/agent, I want to dynamically bundle policies and riders, so that I can offer tailored insurance solutions quickly and efficiently.

Story Points: 13
Priority: Must Have

Acceptance Criteria:
- Customer/agent can select base policy and view compatible riders
- Rider compatibility is validated in real-time
- Bundles are recomputed when riders are added/removed
- Quotes are generated within 5 minutes

Business Rules & Validation Constraints:
- Rider compatibility matrix enforced
- Age, tobacco usage, coverage amount, and duration impact quote

Error Handling & Edge Cases:
- Handle incompatible rider combinations
- Display error messages for invalid age/tobacco usage

US-02: Budget-Capped Package Builder
- Stakeholder: Customer
- FR Origin: FR-1.1.3
- As a customer, I want to build insurance packages within a user-defined budget, so that I can find affordable coverage options.

Story Points: 8
Priority: Must Have

Acceptance Criteria:
- Customer can input maximum monthly/annual budget
- System recommends packages under the specified budget
- Packages include base policies and optional riders

Business Rules & Validation Constraints:
- Budget cap is adhered to for all recommended packages
- Rider costs are factored into total package price

Error Handling & Edge Cases:
- Display error if no packages fit within budget
- Handle zero or negative budget inputs

US-03: Benefit Projection & Comparison
- Stakeholder: Customer
- FR Origin: FR-1.1.5
- As a customer, I want to compare benefits and projections across different packages, so that I can make an informed decision.

Story Points: 5
Priority: Should Have

Acceptance Criteria:
- Side-by-side comparison of base policies and rider benefits
- Projected benefits can be downloaded in a PDF format
- Comparison includes inclusions/exclusions of each rider

Business Rules & Validation Constraints:
- Comparison tool must display key terms and conditions
- PDFs include all relevant policy details

Error Handling & Edge Cases:
- Handle cases where no comparison data is available
- Ensure projections are accurate and up-to-date

US-04: Dynamic Quote Sharing
- Stakeholder: Agent
- FR Origin: FR-1.1.6
- As an agent, I want to easily share quotes with customers via WhatsApp, Email, and SMS, so that I can provide quick follow-ups and support.

Story Points: 3
Priority: Could Have

Acceptance Criteria:
- Agent can generate standardized PDF quote summaries
- System supports direct sharing via WhatsApp, Email, and SMS
- Quotes include key details and contact information

Business Rules & Validation Constraints:
- PDFs adhere to company branding and formatting guidelines
- SMS messages are limited to 160 characters

Error Handling & Edge Cases:
- Handle cases where sharing fails due to invalid customer contact information
- Provide fallback options for failed share attempts

US-05: Actuarial Pricing and Underwriting STP
- Stakeholder: Underwriter
- FR Origin: FR-1.2.2, FR-1.3.3
- As an underwriter, I want to automatically apply multi-rider discounts and enable STP for approved applications, so that I can process policies efficiently.

Story Points: 13
Priority: Must Have

Acceptance Criteria:
- System applies dynamic pricing algorithms and multi-rider discounts
- Applications passing automated checks undergo STP approval
- Underwriters review cases with inconsistencies or threshold breaches

Business Rules & Validation Constraints:
- Discount rules are based on risk combination scores
- STP criteria include risk checks, accumulation limits, and non-medical thresholds

Error Handling & Edge Cases:
- Handle cases where STP approval is not possible
- Provide clear reasons for manual review queue assignment

US-06: Policy Lifecycle Management
- Stakeholder: Administrator
- FR Origin: FR-1.4.1, FR-1.4.2, FR-1.4.3
- As an administrator, I want to manage policy lifecycle components, mid-term alterations, and version control, so that I can maintain policy integrity and compliance.

Story Points: 8
Priority: Must Have

Acceptance Criteria:
- System catalogs and manages policy components from definition to issue
- Supports mid-term inclusions/exclusions of riders and computes premium deltas
- Maintains full version control over rates, terms, and regulatory rules

Business Rules & Validation Constraints:
- Rider inclusions must comply with compatibility matrix
- Rate and term versions are tracked with effective-date stamps

Error Handling & Edge Cases:
- Handle cases where mid-term alterations are not allowed
- Ensure policy data is accurate and up-to-date

US-07: Customer Onboarding and OCR Support
- Stakeholder: Customer Service Representative
- FR Origin: FR-1.5.1
- As a customer service representative, I want to enable automated Video-KYC and document processing, so that I can streamline onboarding and verification processes.

Story Points: 5
Priority: Should Have

Acceptance Criteria:
- System enables automated Video-KYC and digital document upload
- Integrated OCR parsing for identity and financial verification

Business Rules & Validation Constraints:
- Video-KYC and document uploads must meet regulatory standards
- OCR parsing accuracy must be >= 95%

Error Handling & Edge Cases:
- Handle cases where Video-KYC or document upload fails
- Provide fallback options for verification

US-08: Regulatory Compliance and Steering Analytics
- Stakeholder: Compliance Officer
- FR Origin: FR-1.6.1, FR-1.6.2, FR-1.6.3, FR-1.6.4, FR-1.6.5
- As a compliance officer, I want to ensure the platform adheres to regulatory compliance and provides strategic analytics, so that I can maintain legal and business standards.

Story Points: 13
Priority: Must Have

Acceptance Criteria:
- System mandates display and acknowledgment of IRDAI benefit illustrations
- Tracks statutory free-look periods and automates refund calculations
- Integrates e-Signature and captures non-repudiable consent
- Generates and schedules mandatory compliance and regulatory data exports
- Renders real-time executive dashboards with revenue and portfolio metrics

Business Rules & Validation Constraints:
- Benefit illustrations must comply with IRDAI guidelines
- Free-look periods and refunds are calculated based on regulatory timelines
- E-Signatures must be legally binding and secure

Error Handling & Edge Cases:
- Handle cases where compliance data exports fail
- Ensure executive dashboards are up-to-date and accurate

These user story cards cover the key functional requirements categories of Quick Quote Engine, Custom Bundling, Actuarial Pricing, Underwriting STP, and Self-Service Review, along with relevant non-functional requirements. The stories are structured to provide clear acceptance criteria, business rules, and error handling scenarios, ensuring a comprehensive understanding of the system's capabilities and constraints.
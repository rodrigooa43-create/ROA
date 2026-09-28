<!-- BEFORE PUBLISHING, review: (1) the name of the Author/responsible party (Section 2) — for full legal validity, use your full legal name in place of 'ROA'; (2) confirm the contact email. Template: review by an attorney is recommended. -->

# SOFTWARE CONSENT AND USE TERMS

**ROA** — ROA Project
Version of these Terms: 1.0 — Year: 2026

> Read these Terms carefully before installing or using the software. By proceeding with the installation or use, you represent that you have read, understood, and fully agree to all the conditions below. If you do not agree, do not install and do not use the software.

---

## 1. Definitions

For the purposes of these Terms, the following definitions apply:

1.1. **"Software"**: the computer program **ROA**, developed within the scope of the **ROA** project, including its source code and its official versions distributed by the Author.

1.2. **"Author"**: the person identified in Section 2 as responsible for the development and official distribution of the Software.

1.3. **"You," "User," or "Software Operator"**: the natural or legal person who installs, runs, or uses the Software. The term "Software Operator" is used in the lay sense of "the person who operates the program" and is **not** to be confused with the "processor" (operador) figure under the Lei Geral de Proteção de Dados Pessoais (LGPD, the Brazilian General Personal Data Protection Law, Law No. 13.709/2018) (see Section 6).

1.4. **"Participant"**: any third party (volunteer, student, patient, research subject, etc.) from whom the User may collect, record, or process biosignals or other data by means of the Software.

1.5. **"Collected Data"**: the biosignals, recordings, measurements, session metadata, and other data that the User captures, generates, or processes by means of the Software, especially those relating to Participants.

1.6. **"License"**: the open-source license under which the Software is distributed, identified in Section 4.

---

## 2. Identification

2.1. **ROA** is an **open source** computer program and a **NOT-FOR-PROFIT** program, developed within the scope of the **ROA** project.

2.2. Author / Responsible Party: **ROA (personal and independent project)**.

2.3. Contact: **rodrigooa43@gmail.com**.

2.4. Official source code repository: **https://github.com/rodrigooa43-create/OpenBionica**.

2.5. Copyright ownership: **© 2026 ROA**, except as provided in the License addressed in Section 4.

2.6. The Software is distributed free of charge, without any fee, subscription, or paid license.

2.7. **Personal and independent project.** The Software is a **personal and independent** project of the Author, who acts in his own name. The Software **does not represent, does not bind, and does not express the position** of any institution, university, company, public agency, or entity, and no institutional relationship shall be presumed from its use.

---

## 3. What the Software Is and What It Does

3.1. The Software is a tool for the **collection, visualization, and analysis of biosignals** — such as EEG (electroencephalography), EMG (electromyography), ECG (electrocardiography), EoG (electrooculography), and accelerometer data — intended for **research and education**.

3.2. **Purpose.** The Software is intended exclusively for purposes of **scientific research and teaching/learning**. It is neither a commercial nor a clinical product.

3.3. **IMPORTANT STATEMENT — NOT A MEDICAL DEVICE.**
The Software is **NOT a medical device**, has **NOT been certified** by any health regulatory authority, and **MUST NOT be used for diagnosis, treatment, clinical monitoring, or any health-related decision**. The signals, measurements, charts, and analyses it produces are exploratory/educational in nature and **do not replace** the evaluation, opinion, or course of action of a qualified health professional. **Never make clinical decisions based on the Software's results.**

3.4. **Not advice.** The Software and any result, signal, measurement, chart, or analysis produced by it **do not constitute medical, clinical, diagnostic, therapeutic, psychological, legal, scientifically conclusive, or regulatory advice**, and its use **does not create** any physician-patient or professional-client relationship between the Author and the User or the Participants.

3.5. **Electrical safety (hardware).** The Software is *software* only and **does not provide electrical isolation**. **Electrical safety is the responsibility of the amplifier/acquisition board** (isolation, leakage current, applied part), pursuant to standards such as **IEC 60601-1** and the collateral **-2-26** (EEG). Research boards such as the **OpenBCI Cyton are NOT certified** as medical equipment: operate them **battery-powered and isolated from the electrical mains**, **never** connect the participant to a system plugged into a wall outlet (laptop on its charger, grounded USB) without adequate isolation, and follow the hardware manufacturer's instructions. The User is solely responsible for validating the safety of the assembly before any collection involving human beings.

---

## 4. Open Source and Free Nature

4.1. The Software is distributed under the **MIT** license (available at **https://github.com/rodrigooa43-create/OpenBionica/blob/main/LICENSE**).

4.2. Under the terms of such License, you have the right to **use, study, modify, and redistribute** the Software and its source code, subject to the conditions of the applicable License.

4.3. In the event of any conflict between these Terms and the **MIT** License as to the rights of use of the code, **the MIT License shall prevail**. These Terms supplement it with privacy information, disclaimers, and use responsibilities.

4.4. **No additional transfer of rights.** Nothing in these Terms or in the License transfers to the User any patents, trademarks, or any rights not expressly granted by the **MIT** License.

---

## 5. Privacy

5.1. **Local processing.** The Software processes biosignals and other Collected Data **exclusively LOCALLY**, on the machine where it is run (for example, in the `sessions/` folder and in `Documentos/EEG_Coletor`). Such data remains under the exclusive control of the User.

5.2. **No remote processing of Collected Data.** The Software **does NOT perform remote processing, cloud processing, sending, transmission, telemetry, tracking, sharing, or exfiltration** of the Collected Data. No Collected Data of yours is, under any circumstances, sent to the Author or to third parties by the Software.

5.3. **Absence of telemetry in this version.** In the present version of the Software, **there is no telemetry or tracking added by the Author**. Should future versions come to offer any additional network functionality, this will be reported in a prominent manner and will remain under the User's control. Third-party libraries and components have their own policies (see Section 9).

5.4. **Author without access to the data.** The Author **does NOT have access** to any Collected Data of yours through the Software. The Author **does not operate servers** that receive such data and, therefore, does not receive it, does not store it, and cannot see it.

5.5. **Network functionality — manual and optional update check.** The only intentional network functionality of the Software is a **MANUAL and OPTIONAL** update check. In its default configuration, the Software **does not intentionally initiate any network connection to send data**. When — and only when — you manually trigger this check:
- the Software only **DOWNLOADS code** from the official hosting repository/infrastructure (https://github.com/rodrigooa43-create/OpenBionica);
- the Software **does not transmit the Collected Data** nor personal content information;
- as with any internet access, the connection may expose **technical metadata** (for example, IP address, *user-agent*, and date/time) to the repository's hosting provider (for example, GitHub), pursuant to **that third party's privacy policy**;
- this check can be **disabled** and, by default, the Software operates **offline**, without initiating connections to send data.

5.6. **Essential distinction.** There is a difference between (i) the **Collected Data** — which is **never** sent by the Software — and (ii) the **technical connection metadata** (such as the IP address), unavoidably exposed to the hosting provider in any manual update download. The Software's central privacy commitment is: **not to perform remote processing of the Collected Data**.

5.7. **Local record of acceptance.** For traceability purposes, the Software may **store locally, on your own machine**, the version of these Terms and the date/time of acceptance. This record remains **only on your computer** and **is not sent** to anyone.

---

## 6. Data Protection (LGPD) — Roles and Responsibilities

6.1. **You Are the Controller.** If you use the Software to **collect, record, or process Participant data**, **YOU are the controller** of such data, under art. 5, VI, of the **Lei Geral de Proteção de Dados Pessoais — LGPD (Brazilian General Personal Data Protection Law, Law No. 13,709/2018)**, as the party who decides on the purposes and means of the processing. (The term "Software Operator," as used in this document, refers to "whoever operates the program" and does **not** correspond to the "processor" defined in art. 5, VII, of the LGPD.)

6.2. **The Author Is Neither Controller nor Processor.** The Author acts exclusively as a **supplier of a general-purpose software tool**, **does not determine the purposes or the means** of processing of Participants' personal data and, **because the Author has no access to the Collected Data**, **is neither the controller nor the processor** of such processing operations (art. 5, VI and VII, of the LGPD). The Author **is not liable** for any processing, leak, misuse, or legal noncompliance related to the Data Collected by you.

6.3. **Sensitive Personal Data (Biosignals).** You acknowledge that biosignals collected from identified or identifiable persons (EEG, EMG, ECG, EoG, and the like) constitute, as a rule, **SENSITIVE PERSONAL DATA** — data concerning **health** and/or **biometric data** — under **art. 5, II, of the LGPD**, subject to the **heightened regime of art. 11**. As the controller, it is incumbent upon you to ensure a specific legal basis for sensitive data, security measures commensurate with the risk and, where applicable, a **Personal Data Protection Impact Report (RIPD)**.

6.4. **Controller's Responsibilities.** As the controller of the Collected Data, **you are solely responsible** for:

a) **Defining and documenting the appropriate legal basis** for the processing (art. 7 and, for sensitive data, art. 11 of the LGPD), which may be **consent** or another legal ground applicable to your context (for example, the carrying out of studies by a research body) — and, where the basis is consent, **obtaining it from the Participants freely and in an informed and unequivocal manner**;

b) **Defining the purposes** of the processing and processing the data in a manner compatible with them;

c) Ensuring the **safekeeping, security, secrecy, anonymization or pseudonymization** and confidentiality of the data, adopting appropriate **technical and administrative security measures** (art. 46 of the LGPD);

d) **Defining retention periods** and proceeding with the **deletion** of the data upon termination of the processing, except in the cases of retention permitted by law (arts. 15 and 16 of the LGPD);

e) **Meeting data subjects' rights** (art. 18 of the LGPD — access, correction, deletion, portability, etc.); such requests, directed at the Data Collected by you, are your exclusive responsibility, **since the Author has no way of meeting them because the Author has no access to the data**;

f) In the event of a **security incident** that may entail relevant risk or damage, making the **notifications required to the ANPD and to the data subjects** (art. 48 of the LGPD);

g) Observing, in any **international transfers** of the data, the provisions of **art. 33 of the LGPD**;

h) Observing, when collecting data from **children and adolescents**, the specific regime of **art. 14 of the LGPD**, including as to the consent of parents or guardians;

i) Complying with all other **ethical and legal obligations** applicable to your activity and your jurisdiction (including, where applicable, any ethical or institutional approvals that your context may require).

6.5. **Lawful Use.** You undertake to use the Software in a **lawful** manner and in compliance with applicable laws.

---

## 7. Disclaimer of Warranty

7.1. The Software is provided **"AS IS" (*as-is*)** and **"as available"**, **without warranties of any kind**, express or implied.

7.2. **TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE AUTHOR DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, WITHOUT LIMITATION, THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT OF THIRD-PARTY RIGHTS.**

7.3. The Author **does not warrant**, among other things: fitness for a particular purpose, the absence of errors or defects, continuous availability, compatibility with your hardware or system, or the **exactness, precision, clinical or metrological validity, or reliability** of measurements, signals, calculations, or analyses produced. Measurements may contain **noise, artifacts, and errors** and **have no clinical or metrological validity**.

7.4. The Author **does not warrant** that the Software is free of **viruses, malware, or malicious code** introduced by third parties (for example, in copies, *forks*, or unofficial builds, or in the download infrastructure). It is your responsibility to **verify the integrity** of the code or binary obtained, especially in manually downloaded updates.

7.5. You use the Software **at your own risk**.

---

## 8. Limitation of Liability

8.1. To the maximum extent permitted by applicable law, the Author **is not liable** for any **direct, indirect, incidental, special, consequential, or punitive damages** arising out of the use of or the inability to use the Software.

8.2. This includes, without limitation: **loss or corruption of data** and of Collected Data, loss or corruption of biological signals, **artifacts and measurement errors**, interruption of activities, and **decisions made on the basis of the results** generated by the Software.

8.3. **Modified versions and uses outside the intended purpose.** The Author **is not liable** for damages arising from **versions modified by third parties**, *forks*, unofficial builds, third-party integrations, or use of the Software outside the purpose described in Section 3.

8.4. **Liability cap.** Because this is **free Software provided without consideration**, to the maximum extent permitted by applicable law, the Author's **total liability** to the User, for any cause related to the Software, is **limited to R$ 0.00 (zero reais)**.

8.5. **Public policy reservation.** The disclaimers and limitations in these Terms **do not exclude** liabilities that the law mandatorily does not allow to be excluded or limited, such as those arising from **willful misconduct (dolo)**. Should any limitation be deemed inapplicable in a given case, it shall be applied to the **greatest extent permitted** by law, with the remaining provisions preserved (see Section 14).

8.6. You are solely responsible for maintaining **backup copies (backups)** of your data and of the Collected Data.

---

## 9. Indemnification (*Hold Harmless*)

9.1. To the maximum extent permitted by applicable law, you agree to **indemnify, defend, and hold harmless** the Author with respect to any and all claims, losses, damages, fines, penalties, judicial or administrative proceedings (including before the ANPD) and reasonable expenses, including **attorneys' fees**, arising out of or related to:

a) **your use of the Software**;
b) **your violation of these Terms**;
c) the **processing of Participants' data** or of any third parties carried out by you;
d) **your violation of law** or of third-party rights (including the LGPD, personality rights, and research ethics regulations).

9.2. This obligation survives the termination of use of the Software.

---

## 10. Third-Party Components and Licenses

10.1. The Software uses open-source **third-party libraries and components** (for example, libraries from the Python ecosystem and graphical user interface libraries), each subject to **their own licenses**.

10.2. Such third-party licenses remain valid and applicable to the respective components. The Author **does not hold** the rights to these components and **is not liable** for them.

10.3. The notices and texts of the third-party licenses are available at **https://github.com/rodrigooa43-create/OpenBionica/blob/main/THIRD-PARTY-LICENSES.md**. It is recommended that they be consulted, especially with respect to graphical user interface components, which may be subject to specific licenses (for example, LGPL) with implications for the redistribution of the bundle as a whole.

---

## 11. Trademarks and Distinctive Signs

11.1. **"ROA"**, **"ROA"** and their respective logos are **distinctive signs** of the project.

11.2. The code License **does not grant** the right to use the project's trademarks, name, or logos to **endorse, promote, or name** derivative products, *forks*, or unofficial versions, without the Author's prior authorization. Use of the project's name in a manner that suggests official endorsement or misleads third parties is prohibited.

---

## 12. Updates, Support, and Continuity

12.1. Updates are **optional** and depend on manual action by the User (see item 5.5).

12.2. Because this is an **open source and non-profit** project, **there is no obligation** to provide support, maintenance, fixes, new versions, or continuity of the project. **There is no SLA**, response time, or obligation to fix bugs or security flaws.

12.3. The Author may, at any time and without prior notice, **discontinue** development, without this giving rise to any right to compensation. You may continue using the version you have, under the terms of the **MIT** License.

---

## 13. Legal Compliance and Export

13.1. You are responsible for using the Software **in compliance with the applicable laws** in your jurisdiction, including, where applicable, **export and import controls, sanctions** and **rules on research involving human beings and animals**.

13.2. You release the Author from any liability for uses of the Software that **violate** such rules.

---

## 14. General Provisions

14.1. **Capacity.** By accepting these Terms, you represent that you are **at least 18 years of age** (or emancipated) and **fully legally capable** under the terms of the Civil Code. If you accept on behalf of an institution, team, or other legal entity, you represent that you hold sufficient **powers and authority of representation** to bind it to these Terms.

14.2. **Severability (*divisibilidade*).** If any provision of these Terms is held invalid, illegal, or unenforceable, the **remaining provisions shall remain in full force and effect**, and the affected provision shall be interpreted and narrowed to the minimum extent necessary to render it valid, preserving to the greatest extent possible the original intent of the parties.

14.3. **Entire agreement.** These Terms, together with the **MIT** License, constitute the **entire agreement** between you and the Author regarding the use of the Software, superseding any prior understandings or communications on the subject.

14.4. **Amendments to the Terms.** The Author may **revise these Terms** in future versions. The applicable version is the one **accepted at the time of installation or use** of the respective version of the Software. Continued use of a **new version** of the Software, after amendment of the Terms, constitutes **acceptance** of the revised version.

14.5. **Governing law.** These Terms are governed by and construed in accordance with the laws of the **Federative Republic of Brazil**.

14.6. **Venue.** The parties elect the venue (*foro*) of the judicial district (*comarca*) of **the Author's domicile (except for the legally privileged venue, when applicable)** to settle disputes arising from these Terms, **except that**, if by force of mandatory law the User is deemed a consumer or a legally privileged venue exists, **the venue determined by law shall prevail**.

14.7. **Prevailing language.** In the event of translation of these Terms into other languages, the **Portuguese version** shall prevail in case of divergence.

14.8. **Not legal advice.** These Terms are a **template** terms of use and privacy document, drafted in accessible language, and **do not constitute legal advice**. **Review by a legal professional** is recommended, according to the jurisdiction and the specific needs of the Author, prior to public distribution.

## 15. Acceptance

15.1. By installing and/or using the Software, you represent that you have **read, understood, and agree** in full with these Terms of Consent and Use of the Software.

15.2. If you **do not agree** with any condition described herein, **do not install and do not use** the Software.

15.3. For recordkeeping purposes, the Software may **store locally, on your own machine**, the **version of these Terms** and the **date/time of acceptance** (see item 5.7). This record remains **only on your computer** and **is not sent** to anyone.

---

### Acceptance Fields

- **Version of these Terms:** 1.0
- **Year:** 2026
- **Date/time of acceptance:** (automatically recorded upon acceptance)
- **User identification (optional, local record):** (optional)
- [ ] **I have read, understood, and agree** with the Terms of Consent and Use of the Software.

---

> **Notice:** This document is a **template** for terms of use and privacy. It **does not constitute legal advice**. **Review by a legal professional** is recommended, in accordance with the jurisdiction and the specific needs of the Author, prior to public distribution.

---

## Governing Language

This is an English (US) translation of the original Terms, which were written
in Brazilian Portuguese (`TERMO_DE_USO.md`) and are provided with the Software.
This translation is offered for the convenience of readers who do not read
Portuguese. **In the event of any divergence between the two versions, the
Brazilian Portuguese version prevails**, and these Terms remain governed by
Brazilian law as stated above.

# Snapshot text integrity

Snapshot: `v2026.08`. Does a row's `text` hold the whole provision? A supporting
audit, not a chartered milestone, and one that needs **no official oracle** — every
defect below is detectable from the snapshot alone.

## Defect rates

| file | rows | non-null text | truncated head | UI chrome | impossible-title citation |
|---|---:|---:|---:|---:|---:|
| us_ak_constitutions | 243 | 243 | 0 (0.00%) | 0 | 0 |
| us_ak_court_rules | 763 | 763 | 0 (0.00%) | 0 | 0 |
| us_ak_guidance | 398 | 398 | 1 (0.25%) | 0 | 0 |
| us_ak_statutes | 17,935 | 17,935 | 0 (0.00%) | 0 | 2 |
| us_al_constitutions | 381 | 381 | 0 (0.00%) | 0 | 0 |
| us_al_court_rules | 870 | 870 | 0 (0.00%) | 0 | 0 |
| us_al_guidance | 207 | 207 | 0 (0.00%) | 0 | 0 |
| us_al_statutes | 45,984 | 45,984 | 7 (0.02%) | 0 | 0 |
| us_ar_constitutions | 513 | 513 | 0 (0.00%) | 0 | 0 |
| us_ar_guidance | 359 | 359 | 4 (1.11%) | 0 | 0 |
| us_ar_statutes | 36,936 | 36,936 | 5 (0.01%) | 0 | 1 |
| us_az_constitutions | 646 | 646 | 0 (0.00%) | 0 | 0 |
| us_az_court_rules | 1,718 | 1,718 | 107 (6.23%) | 0 | 0 |
| us_az_guidance | 199 | 199 | 0 (0.00%) | 0 | 0 |
| us_az_statutes | 22,674 | 22,674 | 0 (0.00%) | 0 | 0 |
| us_ca_constitutions | 362 | 362 | 0 (0.00%) | 0 | 0 |
| us_ca_court_rules | 1,521 | 1,521 | 0 (0.00%) | 0 | 0 |
| us_ca_guidance | 463 | 463 | 1 (0.22%) | 0 | 1 |
| us_ca_statutes | 161,566 | 161,566 | 6 (0.00%) | 0 | 0 |
| us_co_constitutions | 424 | 424 | 15 (3.54%) | 0 | 0 |
| us_co_regulations | 610 | 610 | 6 (0.98%) | 0 | 2 |
| us_co_statutes | 34,231 | 34,231 | 0 (0.00%) | 0 | 0 |
| us_ct_constitutions | 174 | 174 | 12 (6.90%) | 0 | 0 |
| us_ct_court_rules | 1,723 | 1,723 | 9 (0.52%) | 0 | 0 |
| us_ct_guidance | 369 | 369 | 12 (3.25%) | 0 | 1 |
| us_ct_statutes | 16,082 | 16,082 | 0 (0.00%) | 0 | 0 |
| us_dc_administrative_guidance | 1 | 1 | 0 (0.00%) | 0 | 0 |
| us_dc_court_rules | 1,128 | 1,128 | 6 (0.53%) | 0 | 0 |
| us_dc_guidance | 23 | 23 | 0 (0.00%) | 0 | 0 |
| us_dc_statutes | 23,694 | 23,694 | 0 (0.00%) | 0 | 0 |
| us_de_constitutions | 225 | 225 | 0 (0.00%) | 0 | 0 |
| us_de_court_rules | 1,385 | 1,385 | 4 (0.29%) | 0 | 0 |
| us_de_guidance | 303 | 303 | 0 (0.00%) | 0 | 0 |
| us_de_regulations | 1,164 | 1,164 | 10 (0.86%) | 0 | 1 |
| us_de_statutes | 21,649 | 21,649 | 0 (0.00%) | 0 | 0 |
| us_federal_administrative_guidance | 10 | 10 | 0 (0.00%) | 0 | 0 |
| us_federal_constitutions | 74 | 74 | 0 (0.00%) | 0 | 0 |
| us_federal_court_rules | 589 | 589 | 0 (0.00%) | 0 | 0 |
| us_federal_enforcement_action | 140 | 140 | 0 (0.00%) | 0 | 0 |
| us_federal_executive_order | 738 | 738 | 0 (0.00%) | 0 | 0 |
| us_federal_faq | 444 | 444 | 0 (0.00%) | 0 | 0 |
| us_federal_guidance | 12,364 | 12,364 | 75 (0.61%) | 0 | 91 |
| us_federal_guideline | 302 | 302 | 18 (5.96%) | 0 | 0 |
| us_federal_irs_announcement | 83 | 83 | 0 (0.00%) | 0 | 0 |
| us_federal_irs_notice | 759 | 759 | 0 (0.00%) | 0 | 0 |
| us_federal_irs_rev_proc | 377 | 377 | 0 (0.00%) | 0 | 0 |
| us_federal_irs_rev_rul | 245 | 245 | 0 (0.00%) | 0 | 0 |
| us_federal_memorandum | 401 | 401 | 0 (0.00%) | 0 | 0 |
| us_federal_presidential_document | 655 | 655 | 0 (0.00%) | 0 | 0 |
| us_federal_proclamation | 1,832 | 1,832 | 0 (0.00%) | 0 | 0 |
| us_federal_regulations | 582,054 | 582,054 | 8,011 (1.38%) | 906 | 3,172 |
| us_federal_ruling | 7,248 | 7,248 | 2 (0.03%) | 0 | 48 |
| us_federal_statutes | 54,853 | 54,853 | 1 (0.00%) | 0 | 17 |
| us_federal_treaty | 119 | 119 | 2 (1.68%) | 0 | 1 |
| us_fl_constitutions | 217 | 217 | 0 (0.00%) | 0 | 0 |
| us_fl_court_rules | 936 | 936 | 2 (0.21%) | 0 | 0 |
| us_fl_guidance | 43 | 43 | 0 (0.00%) | 0 | 0 |
| us_fl_statutes | 24,866 | 24,866 | 2 (0.01%) | 0 | 0 |
| us_ga_constitutions | 287 | 287 | 0 (0.00%) | 0 | 0 |
| us_ga_court_rules | 1,174 | 1,174 | 39 (3.32%) | 0 | 0 |
| us_ga_guidance | 66 | 66 | 1 (1.52%) | 0 | 0 |
| us_hi_constitutions | 171 | 171 | 1 (0.58%) | 0 | 0 |
| us_hi_court_rules | 1,259 | 1,259 | 1 (0.08%) | 0 | 0 |
| us_hi_guidance | 168 | 168 | 0 (0.00%) | 0 | 1 |
| us_hi_statutes | 19,197 | 19,197 | 3 (0.02%) | 0 | 0 |
| us_ia_constitutions | 190 | 190 | 0 (0.00%) | 0 | 0 |
| us_ia_court_rules | 1,294 | 1,294 | 593 (45.83%) | 0 | 0 |
| us_ia_guidance | 83 | 83 | 0 (0.00%) | 0 | 0 |
| us_ia_statutes | 28,223 | 28,223 | 0 (0.00%) | 0 | 0 |
| us_id_constitutions | 240 | 240 | 2 (0.83%) | 0 | 0 |
| us_id_court_rules | 766 | 766 | 1 (0.13%) | 0 | 0 |
| us_id_guidance | 75 | 75 | 0 (0.00%) | 0 | 0 |
| us_id_regulations | 8,551 | 8,551 | 1 (0.01%) | 0 | 10 |
| us_id_statutes | 22,754 | 22,754 | 4 (0.02%) | 0 | 0 |
| us_il_constitutions | 170 | 170 | 0 (0.00%) | 0 | 0 |
| us_il_court_rules | 839 | 839 | 0 (0.00%) | 0 | 0 |
| us_il_guidance | 158 | 158 | 0 (0.00%) | 0 | 0 |
| us_il_regulations | 53,584 | 53,584 | 73 (0.14%) | 0 | 8 |
| us_il_statutes | 72,456 | 72,456 | 0 (0.00%) | 0 | 4 |
| us_in_constitutions | 196 | 196 | 0 (0.00%) | 0 | 0 |
| us_in_court_rules | 879 | 879 | 4 (0.46%) | 0 | 0 |
| us_in_guidance | 281 | 281 | 0 (0.00%) | 0 | 0 |
| us_in_statutes | 83,148 | 83,148 | 0 (0.00%) | 0 | 0 |
| us_ks_constitutions | 229 | 229 | 0 (0.00%) | 0 | 0 |
| us_ks_court_rules | 434 | 434 | 0 (0.00%) | 0 | 0 |
| us_ks_guidance | 79 | 79 | 1 (1.27%) | 0 | 0 |
| us_ks_statutes | 24,361 | 24,361 | 0 (0.00%) | 0 | 0 |
| us_ky_constitutions | 274 | 274 | 0 (0.00%) | 0 | 0 |
| us_ky_guidance | 232 | 232 | 0 (0.00%) | 0 | 0 |
| us_ky_regulations | 4,865 | 4,865 | 28 (0.58%) | 0 | 2 |
| us_ky_statutes | 20,894 | 20,894 | 0 (0.00%) | 0 | 0 |
| us_la_constitutions | 328 | 328 | 1 (0.30%) | 0 | 0 |
| us_la_court_rules | 481 | 481 | 9 (1.87%) | 0 | 0 |
| us_la_statutes | 43,512 | 43,512 | 53 (0.12%) | 0 | 0 |
| us_ma_constitutions | 104 | 104 | 0 (0.00%) | 0 | 0 |
| us_ma_court_rules | 970 | 970 | 0 (0.00%) | 0 | 0 |
| us_ma_guidance | 417 | 417 | 0 (0.00%) | 0 | 0 |
| us_ma_statutes | 23,152 | 23,152 | 0 (0.00%) | 0 | 0 |
| us_md_constitutions | 312 | 312 | 0 (0.00%) | 0 | 0 |
| us_md_court_rules | 1,220 | 1,220 | 0 (0.00%) | 0 | 0 |
| us_md_guidance | 675 | 675 | 5 (0.74%) | 0 | 0 |
| us_md_regulations | 12,863 | 12,863 | 20 (0.16%) | 0 | 0 |
| us_md_statutes | 39,552 | 39,552 | 0 (0.00%) | 0 | 0 |
| us_me_constitutions | 153 | 153 | 0 (0.00%) | 0 | 0 |
| us_me_court_rules | 722 | 722 | 25 (3.46%) | 0 | 0 |
| us_me_guidance | 228 | 228 | 0 (0.00%) | 0 | 0 |
| us_me_regulations | 1,718 | 1,718 | 52 (3.03%) | 0 | 0 |
| us_me_statutes | 25,316 | 25,316 | 2 (0.01%) | 0 | 1 |
| us_mi_constitutions | 307 | 307 | 0 (0.00%) | 0 | 0 |
| us_mi_court_rules | 1,025 | 1,025 | 24 (2.34%) | 0 | 0 |
| us_mi_guidance | 145 | 145 | 0 (0.00%) | 0 | 0 |
| us_mi_statutes | 40,658 | 40,658 | 12 (0.03%) | 0 | 0 |
| us_mn_constitutions | 138 | 138 | 0 (0.00%) | 0 | 0 |
| us_mn_court_rules | 958 | 958 | 0 (0.00%) | 0 | 0 |
| us_mn_guidance | 34 | 34 | 2 (5.88%) | 0 | 0 |
| us_mn_regulations | 15,447 | 15,447 | 6 (0.04%) | 0 | 1 |
| us_mn_statutes | 27,747 | 27,747 | 0 (0.00%) | 0 | 0 |
| us_mo_constitutions | 445 | 445 | 0 (0.00%) | 0 | 0 |
| us_mo_guidance | 106 | 106 | 1 (0.94%) | 0 | 0 |
| us_mo_statutes | 29,309 | 29,309 | 1 (0.00%) | 0 | 0 |
| us_ms_constitutions | 318 | 318 | 0 (0.00%) | 0 | 0 |
| us_ms_court_rules | 794 | 794 | 43 (5.42%) | 0 | 0 |
| us_ms_guidance | 240 | 240 | 0 (0.00%) | 0 | 0 |
| us_ms_statutes | 158,688 | 158,688 | 0 (0.00%) | 0 | 24 |
| us_mt_constitutions | 196 | 196 | 0 (0.00%) | 0 | 0 |
| us_mt_court_rules | 238 | 238 | 0 (0.00%) | 0 | 0 |
| us_mt_guidance | 149 | 149 | 0 (0.00%) | 0 | 0 |
| us_mt_statutes | 30,514 | 30,514 | 0 (0.00%) | 0 | 0 |
| us_nc_constitutions | 155 | 155 | 0 (0.00%) | 0 | 0 |
| us_nc_court_rules | 495 | 495 | 1 (0.20%) | 0 | 0 |
| us_nc_guidance | 120 | 120 | 0 (0.00%) | 0 | 0 |
| us_nd_constitutions | 203 | 203 | 0 (0.00%) | 0 | 0 |
| us_nd_court_rules | 2,246 | 2,246 | 2 (0.09%) | 0 | 0 |
| us_nd_guidance | 235 | 235 | 0 (0.00%) | 0 | 1 |
| us_nd_statutes | 29,042 | 29,042 | 0 (0.00%) | 0 | 0 |
| us_ne_constitutions | 448 | 448 | 0 (0.00%) | 0 | 0 |
| us_ne_court_rules | 734 | 734 | 0 (0.00%) | 0 | 0 |
| us_ne_guidance | 120 | 120 | 0 (0.00%) | 0 | 0 |
| us_ne_statutes | 25,997 | 25,997 | 0 (0.00%) | 0 | 0 |
| us_nh_constitutions | 157 | 157 | 0 (0.00%) | 0 | 0 |
| us_nh_court_rules | 970 | 970 | 7 (0.72%) | 0 | 0 |
| us_nh_guidance | 177 | 177 | 3 (1.69%) | 0 | 0 |
| us_nh_statutes | 25,375 | 25,375 | 0 (0.00%) | 0 | 0 |
| us_nj_constitutions | 216 | 216 | 6 (2.78%) | 0 | 0 |
| us_nj_guidance | 441 | 441 | 0 (0.00%) | 0 | 0 |
| us_nj_statutes | 55,993 | 55,993 | 1,697 (3.03%) | 0 | 2 |
| us_nm_constitutions | 299 | 299 | 0 (0.00%) | 0 | 0 |
| us_nm_guidance | 274 | 274 | 0 (0.00%) | 0 | 0 |
| us_nm_regulations | 13,270 | 13,270 | 7 (0.05%) | 0 | 0 |
| us_nm_statutes | 34,455 | 34,455 | 0 (0.00%) | 0 | 0 |
| us_nv_constitutions | 234 | 234 | 0 (0.00%) | 0 | 0 |
| us_nv_court_rules | 1,338 | 1,338 | 1 (0.07%) | 0 | 0 |
| us_nv_guidance | 199 | 199 | 1 (0.50%) | 0 | 0 |
| us_nv_statutes | 48,190 | 48,190 | 0 (0.00%) | 0 | 0 |
| us_ny_constitutions | 204 | 204 | 0 (0.00%) | 0 | 0 |
| us_ny_court_rules | 1,088 | 1,088 | 4 (0.37%) | 0 | 1 |
| us_ny_guidance | 1,199 | 1,199 | 0 (0.00%) | 0 | 0 |
| us_ny_statutes | 40,140 | 40,140 | 0 (0.00%) | 0 | 4 |
| us_oh_constitutions | 266 | 266 | 0 (0.00%) | 0 | 0 |
| us_oh_court_rules | 1,167 | 1,167 | 153 (13.11%) | 0 | 0 |
| us_oh_guidance | 112 | 112 | 0 (0.00%) | 0 | 0 |
| us_oh_regulations | 19,909 | 19,909 | 57 (0.29%) | 0 | 7 |
| us_oh_statutes | 33,161 | 33,161 | 0 (0.00%) | 0 | 0 |
| us_ok_constitutions | 545 | 545 | 0 (0.00%) | 0 | 0 |
| us_ok_guidance | 144 | 144 | 0 (0.00%) | 0 | 0 |
| us_ok_statutes | 35,329 | 35,329 | 6,720 (19.02%) | 0 | 3 |
| us_or_constitutions | 415 | 415 | 0 (0.00%) | 0 | 0 |
| us_or_court_rules | 632 | 632 | 1 (0.16%) | 0 | 0 |
| us_or_guidance | 92 | 92 | 6 (6.52%) | 0 | 0 |
| us_or_statutes | 36,202 | 36,202 | 1 (0.00%) | 0 | 0 |
| us_pa_constitutions | 186 | 186 | 7 (3.76%) | 0 | 0 |
| us_pa_court_rules | 1,722 | 1,722 | 0 (0.00%) | 0 | 0 |
| us_pa_statutes | 14,571 | 14,571 | 2 (0.01%) | 0 | 0 |
| us_pr_constitutions | 102 | 102 | 0 (0.00%) | 0 | 0 |
| us_pr_court_rules | 1,528 | 1,528 | 80 (5.24%) | 0 | 0 |
| us_pr_guidance | 1,641 | 1,641 | 1 (0.06%) | 0 | 0 |
| us_pr_statutes | 23,636 | 23,636 | 715 (3.03%) | 0 | 0 |
| us_ri_constitutions | 118 | 118 | 0 (0.00%) | 0 | 0 |
| us_ri_court_rules | 1,033 | 1,033 | 304 (29.43%) | 0 | 0 |
| us_ri_guidance | 134 | 134 | 0 (0.00%) | 0 | 0 |
| us_ri_statutes | 21,107 | 21,107 | 1 (0.00%) | 0 | 0 |
| us_sc_constitutions | 245 | 245 | 3 (1.22%) | 0 | 0 |
| us_sc_court_rules | 557 | 557 | 0 (0.00%) | 0 | 0 |
| us_sc_guidance | 319 | 319 | 2 (0.63%) | 0 | 0 |
| us_sc_regulations | 6,606 | 6,606 | 8 (0.12%) | 0 | 0 |
| us_sc_statutes | 29,947 | 29,947 | 0 (0.00%) | 0 | 0 |
| us_sd_constitutions | 294 | 294 | 0 (0.00%) | 0 | 0 |
| us_sd_guidance | 27 | 27 | 0 (0.00%) | 0 | 0 |
| us_sd_regulations | 28,988 | 28,988 | 1 (0.00%) | 0 | 0 |
| us_sd_statutes | 39,589 | 39,589 | 1 (0.00%) | 0 | 0 |
| us_tn_constitutions | 152 | 152 | 0 (0.00%) | 0 | 0 |
| us_tn_court_rules | 626 | 626 | 1 (0.16%) | 0 | 0 |
| us_tn_guidance | 173 | 173 | 17 (9.83%) | 0 | 0 |
| us_tn_statutes | 32,693 | 32,693 | 9 (0.03%) | 0 | 0 |
| us_tx_constitutions | 401 | 401 | 0 (0.00%) | 0 | 0 |
| us_tx_court_rules | 1,007 | 1,007 | 0 (0.00%) | 0 | 0 |
| us_tx_guidance | 1,254 | 1,254 | 1 (0.08%) | 0 | 1 |
| us_tx_regulations | 44,247 | 44,247 | 0 (0.00%) | 0 | 4 |
| us_tx_statutes | 122,535 | 122,535 | 0 (0.00%) | 0 | 0 |
| us_ut_constitutions | 189 | 189 | 0 (0.00%) | 0 | 0 |
| us_ut_court_rules | 919 | 919 | 1 (0.11%) | 0 | 0 |
| us_ut_guidance | 168 | 168 | 0 (0.00%) | 0 | 0 |
| us_ut_statutes | 25,880 | 25,880 | 0 (0.00%) | 0 | 0 |
| us_va_constitutions | 134 | 134 | 0 (0.00%) | 0 | 0 |
| us_va_court_rules | 358 | 358 | 7 (1.96%) | 0 | 0 |
| us_va_guidance | 89 | 89 | 1 (1.12%) | 0 | 0 |
| us_va_regulations | 22,396 | 22,396 | 5 (0.02%) | 0 | 5 |
| us_va_statutes | 33,857 | 33,857 | 0 (0.00%) | 0 | 0 |
| us_vt_constitutions | 120 | 120 | 0 (0.00%) | 0 | 0 |
| us_vt_guidance | 187 | 187 | 0 (0.00%) | 0 | 0 |
| us_vt_statutes | 23,521 | 23,521 | 0 (0.00%) | 0 | 1 |
| us_wa_constitutions | 282 | 282 | 0 (0.00%) | 0 | 0 |
| us_wa_court_rules | 1,182 | 1,182 | 0 (0.00%) | 0 | 0 |
| us_wa_guidance | 24 | 24 | 1 (4.17%) | 0 | 0 |
| us_wa_regulations | 51,026 | 51,026 | 117 (0.23%) | 0 | 4 |
| us_wa_statutes | 51,498 | 51,498 | 0 (0.00%) | 0 | 1 |
| us_wi_constitutions | 175 | 175 | 0 (0.00%) | 0 | 0 |
| us_wi_court_rules | 395 | 395 | 2 (0.51%) | 0 | 0 |
| us_wi_guidance | 232 | 232 | 0 (0.00%) | 0 | 0 |
| us_wi_regulations | 17,823 | 17,823 | 1 (0.01%) | 0 | 1 |
| us_wi_statutes | 18,158 | 18,158 | 13 (0.07%) | 0 | 0 |
| us_wv_constitutions | 209 | 209 | 0 (0.00%) | 0 | 0 |
| us_wv_court_rules | 1,116 | 1,116 | 1 (0.09%) | 0 | 0 |
| us_wv_guidance | 174 | 174 | 0 (0.00%) | 0 | 0 |
| us_wv_statutes | 25,664 | 25,664 | 16 (0.06%) | 0 | 0 |
| us_wy_constitutions | 316 | 316 | 1 (0.32%) | 0 | 0 |
| us_wy_court_rules | 1,010 | 1,010 | 0 (0.00%) | 0 | 0 |
| us_wy_guidance | 62 | 62 | 0 (0.00%) | 0 | 0 |
| us_wy_statutes | 20,999 | 20,999 | 4 (0.02%) | 0 | 0 |

`truncated head` = the body begins with a lowercase letter, i.e. mid-word. `UI chrome` = the body carries the eCFR banner `Link to an amendment published…`, website furniture captured as legal text. `impossible-title citation` = a digit run adjacent to a code token straight after a newline (`\n0 CFR 264.100`, really 40 CFR).

## Repeated spans

A block of 395-402 characters stated **twice, back to back across a newline**. `checkable` is rows long enough to hold two copies plus the separator and containing a newline — the exact precondition for the defect, so it is the denominator the rate is against; scoring it against every row would dilute it with rows the defect cannot reach.

| file | checkable rows | rows with a repeated span | blocks | repeated characters |
|---|---:|---:|---:|---:|
| us_ak_constitutions | 11 | 11 (100.00%) | 34 | 13,596 |
| us_ak_court_rules | 569 | 392 (68.89%) | 1,547 | 617,537 |
| us_ak_guidance | 395 | 320 (81.01%) | 1,123 | 448,593 |
| us_ak_statutes | 7,718 | 933 (12.09%) | 1,455 | 581,750 |
| us_al_constitutions | 82 | 82 (100.00%) | 233 | 93,155 |
| us_al_court_rules | 717 | 523 (72.94%) | 2,547 | 1,016,859 |
| us_al_guidance | 202 | 150 (74.26%) | 438 | 175,123 |
| us_al_statutes | 16,069 | 2,687 (16.72%) | 4,710 | 1,883,184 |
| us_ar_constitutions | 29 | 27 (93.10%) | 105 | 41,986 |
| us_ar_guidance | 357 | 280 (78.43%) | 875 | 349,565 |
| us_ar_statutes | 27,929 | 10,114 (36.21%) | 27,180 | 10,867,187 |
| us_az_constitutions | 52 | 52 (100.00%) | 126 | 50,381 |
| us_az_court_rules | 597 | 597 (100.00%) | 1,676 | 670,028 |
| us_az_guidance | 199 | 192 (96.48%) | 1,448 | 578,796 |
| us_az_statutes | 14,079 | 2,380 (16.90%) | 4,209 | 1,682,873 |
| us_ca_constitutions | 64 | 64 (100.00%) | 163 | 65,177 |
| us_ca_court_rules | 698 | 698 (100.00%) | 1,921 | 768,031 |
| us_ca_guidance | 457 | 385 (84.25%) | 1,678 | 670,284 |
| us_ca_statutes | 54,896 | 8,757 (15.95%) | 15,404 | 6,159,064 |
| us_co_constitutions | 59 | 58 (98.31%) | 139 | 55,578 |
| us_co_regulations | 383 | 366 (95.56%) | 16,725 | 6,687,355 |
| us_co_statutes | 17,390 | 4,647 (26.72%) | 9,455 | 3,780,430 |
| us_ct_constitutions | 17 | 17 (100.00%) | 35 | 13,987 |
| us_ct_court_rules | 791 | 351 (44.37%) | 1,037 | 414,488 |
| us_ct_guidance | 360 | 314 (87.22%) | 1,207 | 482,251 |
| us_ct_statutes | 9,415 | 2,654 (28.19%) | 5,701 | 2,279,436 |
| us_dc_administrative_guidance | 0 | 0 (—) | 0 | 0 |
| us_dc_court_rules | 748 | 467 (62.43%) | 1,368 | 545,988 |
| us_dc_guidance | 23 | 21 (91.30%) | 64 | 25,582 |
| us_dc_statutes | 9,636 | 4,331 (44.95%) | 10,678 | 4,269,038 |
| us_de_constitutions | 21 | 21 (100.00%) | 35 | 13,993 |
| us_de_court_rules | 817 | 492 (60.22%) | 1,642 | 655,296 |
| us_de_guidance | 300 | 237 (79.00%) | 781 | 312,123 |
| us_de_regulations | 1,044 | 953 (91.28%) | 21,317 | 8,522,937 |
| us_de_statutes | 10,310 | 1,821 (17.66%) | 3,319 | 1,326,988 |
| us_federal_administrative_guidance | 0 | 0 (—) | 0 | 0 |
| us_federal_constitutions | 0 | 0 (—) | 0 | 0 |
| us_federal_court_rules | 295 | 0 (0.00%) | 0 | 0 |
| us_federal_enforcement_action | 92 | 53 (57.61%) | 696 | 278,124 |
| us_federal_executive_order | 738 | 725 (98.24%) | 4,868 | 1,945,304 |
| us_federal_faq | 254 | 78 (30.71%) | 121 | 48,374 |
| us_federal_guidance | 10,463 | 8,155 (77.94%) | 79,823 | 31,895,863 |
| us_federal_guideline | 183 | 146 (79.78%) | 567 | 226,707 |
| us_federal_irs_announcement | 82 | 77 (93.90%) | 772 | 308,592 |
| us_federal_irs_notice | 759 | 754 (99.34%) | 9,394 | 3,753,027 |
| us_federal_irs_rev_proc | 377 | 371 (98.41%) | 12,733 | 5,079,929 |
| us_federal_irs_rev_rul | 245 | 245 (100.00%) | 1,502 | 600,086 |
| us_federal_memorandum | 400 | 266 (66.50%) | 876 | 350,060 |
| us_federal_presidential_document | 652 | 525 (80.52%) | 1,025 | 409,539 |
| us_federal_proclamation | 1,831 | 1,782 (97.32%) | 6,232 | 2,490,101 |
| us_federal_regulations | 474,442 | 242,039 (51.02%) | 5,034,563 | 2,012,273,080 |
| us_federal_ruling | 1,380 | 1,341 (97.17%) | 13,732 | 5,488,486 |
| us_federal_statutes | 41,555 | 26,426 (63.59%) | 157,165 | 62,838,956 |
| us_federal_treaty | 119 | 119 (100.00%) | 10,014 | 4,002,837 |
| us_fl_constitutions | 43 | 43 (100.00%) | 103 | 41,181 |
| us_fl_court_rules | 747 | 511 (68.41%) | 2,451 | 980,005 |
| us_fl_guidance | 43 | 33 (76.74%) | 71 | 28,361 |
| us_fl_statutes | 16,453 | 4,532 (27.55%) | 10,697 | 4,277,099 |
| us_ga_constitutions | 29 | 29 (100.00%) | 71 | 28,388 |
| us_ga_court_rules | 471 | 209 (44.37%) | 567 | 226,342 |
| us_ga_guidance | 65 | 31 (47.69%) | 59 | 23,572 |
| us_hi_constitutions | 9 | 9 (100.00%) | 16 | 6,399 |
| us_hi_court_rules | 721 | 406 (56.31%) | 1,354 | 541,384 |
| us_hi_guidance | 167 | 142 (85.03%) | 567 | 226,427 |
| us_hi_statutes | 9,498 | 1,395 (14.69%) | 2,126 | 850,057 |
| us_ia_constitutions | 2 | 2 (100.00%) | 2 | 800 |
| us_ia_court_rules | 586 | 292 (49.83%) | 809 | 323,450 |
| us_ia_guidance | 82 | 63 (76.83%) | 213 | 85,069 |
| us_ia_statutes | 13,171 | 2,192 (16.64%) | 4,046 | 1,617,703 |
| us_id_constitutions | 2 | 2 (100.00%) | 2 | 800 |
| us_id_court_rules | 483 | 302 (62.53%) | 850 | 339,849 |
| us_id_guidance | 75 | 52 (69.33%) | 136 | 54,346 |
| us_id_regulations | 1,799 | 1,799 (100.00%) | 5,022 | 2,007,940 |
| us_id_statutes | 13,233 | 1,746 (13.19%) | 2,844 | 1,137,128 |
| us_il_constitutions | 9 | 9 (100.00%) | 13 | 5,194 |
| us_il_court_rules | 751 | 548 (72.97%) | 2,604 | 1,041,184 |
| us_il_guidance | 158 | 136 (86.08%) | 495 | 197,822 |
| us_il_regulations | 29,377 | 14,555 (49.55%) | 43,276 | 17,297,894 |
| us_il_statutes | 2,661 | 2,527 (94.96%) | 4,962 | 1,983,822 |
| us_in_constitutions | 4 | 4 (100.00%) | 7 | 2,800 |
| us_in_court_rules | 611 | 418 (68.41%) | 1,628 | 650,915 |
| us_in_guidance | 253 | 181 (71.54%) | 408 | 162,963 |
| us_in_statutes | 24,954 | 2,013 (8.07%) | 2,941 | 1,175,915 |
| us_ks_constitutions | 21 | 21 (100.00%) | 62 | 24,780 |
| us_ks_court_rules | 322 | 205 (63.66%) | 620 | 247,896 |
| us_ks_guidance | 79 | 46 (58.23%) | 172 | 68,654 |
| us_ks_statutes | 10,926 | 2,153 (19.71%) | 3,774 | 1,508,964 |
| us_ky_constitutions | 74 | 11 (14.86%) | 13 | 5,194 |
| us_ky_guidance | 229 | 208 (90.83%) | 1,348 | 538,359 |
| us_ky_regulations | 3,113 | 3,093 (99.36%) | 20,594 | 8,234,194 |
| us_ky_statutes | 12,479 | 2,089 (16.74%) | 3,490 | 1,395,391 |
| us_la_constitutions | 57 | 57 (100.00%) | 166 | 66,370 |
| us_la_court_rules | 216 | 113 (52.31%) | 649 | 259,381 |
| us_la_statutes | 23,523 | 4,526 (19.24%) | 8,640 | 3,454,553 |
| us_ma_constitutions | 8 | 8 (100.00%) | 81 | 32,381 |
| us_ma_court_rules | 698 | 501 (71.78%) | 2,699 | 1,079,066 |
| us_ma_guidance | 416 | 376 (90.38%) | 1,835 | 733,529 |
| us_ma_statutes | 18,093 | 5,419 (29.95%) | 13,282 | 5,310,503 |
| us_md_constitutions | 36 | 36 (100.00%) | 89 | 35,581 |
| us_md_court_rules | 872 | 478 (54.82%) | 1,156 | 462,189 |
| us_md_guidance | 672 | 546 (81.25%) | 3,134 | 1,251,986 |
| us_md_regulations | 8,413 | 4,566 (54.27%) | 12,438 | 4,973,129 |
| us_md_statutes | 19,377 | 2,446 (12.62%) | 4,619 | 1,846,783 |
| us_me_constitutions | 13 | 13 (100.00%) | 25 | 9,995 |
| us_me_court_rules | 503 | 318 (63.22%) | 1,071 | 427,239 |
| us_me_guidance | 228 | 193 (84.65%) | 575 | 229,778 |
| us_me_regulations | 1,531 | 1,444 (94.32%) | 22,968 | 9,183,127 |
| us_me_statutes | 13,544 | 3,323 (24.53%) | 6,371 | 2,547,275 |
| us_mi_constitutions | 17 | 17 (100.00%) | 41 | 16,398 |
| us_mi_court_rules | 708 | 437 (61.72%) | 1,548 | 618,665 |
| us_mi_guidance | 145 | 117 (80.69%) | 525 | 209,698 |
| us_mi_statutes | 22,277 | 3,696 (16.59%) | 6,941 | 2,775,251 |
| us_mn_constitutions | 0 | 0 (—) | 0 | 0 |
| us_mn_court_rules | 385 | 384 (99.74%) | 1,440 | 575,654 |
| us_mn_guidance | 34 | 29 (85.29%) | 173 | 69,122 |
| us_mn_regulations | 4,554 | 4,542 (99.74%) | 13,478 | 5,388,746 |
| us_mn_statutes | 15,803 | 4,653 (29.44%) | 10,006 | 4,000,615 |
| us_mo_constitutions | 48 | 46 (95.83%) | 258 | 103,145 |
| us_mo_guidance | 106 | 87 (82.08%) | 211 | 84,244 |
| us_mo_statutes | 17,888 | 2,884 (16.12%) | 4,946 | 1,977,527 |
| us_ms_constitutions | 16 | 16 (100.00%) | 34 | 13,594 |
| us_ms_court_rules | 556 | 335 (60.25%) | 1,060 | 423,478 |
| us_ms_guidance | 239 | 191 (79.92%) | 648 | 259,069 |
| us_ms_statutes | 66,593 | 15,209 (22.84%) | 25,861 | 10,340,216 |
| us_mt_constitutions | 2 | 2 (100.00%) | 2 | 800 |
| us_mt_court_rules | 135 | 76 (56.30%) | 195 | 77,967 |
| us_mt_guidance | 149 | 121 (81.21%) | 658 | 262,956 |
| us_mt_statutes | 13,753 | 1,354 (9.85%) | 2,504 | 1,001,185 |
| us_nc_constitutions | 7 | 6 (85.71%) | 7 | 2,799 |
| us_nc_court_rules | 384 | 260 (67.71%) | 1,147 | 457,961 |
| us_nc_guidance | 119 | 62 (52.10%) | 168 | 67,121 |
| us_nd_constitutions | 8 | 8 (100.00%) | 18 | 7,197 |
| us_nd_court_rules | 1,773 | 1,294 (72.98%) | 4,102 | 1,640,145 |
| us_nd_guidance | 222 | 160 (72.07%) | 659 | 263,447 |
| us_nd_statutes | 11,459 | 1,086 (9.48%) | 1,846 | 738,073 |
| us_ne_constitutions | 47 | 47 (100.00%) | 68 | 27,192 |
| us_ne_court_rules | 466 | 271 (58.15%) | 829 | 331,432 |
| us_ne_guidance | 118 | 95 (80.51%) | 367 | 146,641 |
| us_ne_statutes | 13,902 | 2,077 (14.94%) | 4,677 | 1,869,780 |
| us_nh_constitutions | 7 | 7 (100.00%) | 38 | 15,193 |
| us_nh_court_rules | 529 | 315 (59.55%) | 1,137 | 454,606 |
| us_nh_guidance | 175 | 138 (78.86%) | 689 | 275,246 |
| us_nh_statutes | 1,460 | 1,460 (100.00%) | 2,465 | 985,588 |
| us_nj_constitutions | 24 | 24 (100.00%) | 117 | 46,777 |
| us_nj_guidance | 440 | 378 (85.91%) | 1,336 | 533,831 |
| us_nj_statutes | 4,119 | 3,545 (86.06%) | 5,826 | 2,329,379 |
| us_nm_constitutions | 23 | 23 (100.00%) | 45 | 17,994 |
| us_nm_guidance | 270 | 236 (87.41%) | 615 | 245,666 |
| us_nm_regulations | 2,388 | 2,388 (100.00%) | 8,561 | 3,422,912 |
| us_nm_statutes | 14,164 | 1,805 (12.74%) | 2,621 | 1,047,942 |
| us_nv_constitutions | 36 | 36 (100.00%) | 68 | 27,177 |
| us_nv_court_rules | 429 | 429 (100.00%) | 1,038 | 414,995 |
| us_nv_guidance | 195 | 122 (62.56%) | 410 | 163,862 |
| us_nv_statutes | 19,994 | 1,603 (8.02%) | 2,130 | 851,600 |
| us_ny_constitutions | 47 | 46 (97.87%) | 97 | 38,783 |
| us_ny_court_rules | 582 | 301 (51.72%) | 892 | 356,646 |
| us_ny_guidance | 1,193 | 909 (76.19%) | 4,261 | 1,703,544 |
| us_ny_statutes | 7,415 | 7,404 (99.85%) | 19,354 | 7,738,150 |
| us_oh_constitutions | 51 | 51 (100.00%) | 154 | 61,570 |
| us_oh_court_rules | 706 | 369 (52.27%) | 1,626 | 648,547 |
| us_oh_guidance | 107 | 89 (83.18%) | 220 | 87,956 |
| us_oh_regulations | 10,219 | 10,212 (99.93%) | 39,285 | 15,707,470 |
| us_oh_statutes | 6 | 0 (0.00%) | 0 | 0 |
| us_ok_constitutions | 69 | 69 (100.00%) | 177 | 70,761 |
| us_ok_guidance | 143 | 106 (74.13%) | 334 | 133,344 |
| us_ok_statutes | 17,436 | 3,269 (18.75%) | 6,261 | 2,503,121 |
| us_or_constitutions | 37 | 37 (100.00%) | 86 | 34,391 |
| us_or_court_rules | 381 | 189 (49.61%) | 791 | 315,658 |
| us_or_guidance | 92 | 81 (88.04%) | 351 | 140,238 |
| us_or_statutes | 26,018 | 3,203 (12.31%) | 4,872 | 1,947,984 |
| us_pa_constitutions | 11 | 11 (100.00%) | 21 | 8,399 |
| us_pa_court_rules | 729 | 729 (100.00%) | 2,110 | 843,625 |
| us_pa_statutes | 7,822 | 1,455 (18.60%) | 2,399 | 959,208 |
| us_pr_constitutions | 3 | 3 (100.00%) | 5 | 1,998 |
| us_pr_court_rules | 758 | 310 (40.90%) | 803 | 320,744 |
| us_pr_guidance | 1,599 | 1,163 (72.73%) | 4,733 | 1,891,762 |
| us_pr_statutes | 0 | 0 (—) | 0 | 0 |
| us_ri_constitutions | 1 | 1 (100.00%) | 2 | 800 |
| us_ri_court_rules | 611 | 335 (54.83%) | 898 | 358,324 |
| us_ri_guidance | 132 | 110 (83.33%) | 437 | 174,517 |
| us_ri_statutes | 6,748 | 1,057 (15.66%) | 1,759 | 703,258 |
| us_sc_constitutions | 14 | 14 (100.00%) | 23 | 9,200 |
| us_sc_court_rules | 424 | 276 (65.09%) | 1,022 | 408,621 |
| us_sc_guidance | 314 | 284 (90.45%) | 1,412 | 564,052 |
| us_sc_regulations | 2,892 | 1,506 (52.07%) | 8,564 | 3,423,672 |
| us_sc_statutes | 1,931 | 1,930 (99.95%) | 3,077 | 1,230,253 |
| us_sd_constitutions | 27 | 27 (100.00%) | 146 | 58,380 |
| us_sd_guidance | 26 | 13 (50.00%) | 19 | 7,594 |
| us_sd_regulations | 4,864 | 999 (20.54%) | 1,808 | 722,892 |
| us_sd_statutes | 10,722 | 324 (3.02%) | 678 | 271,083 |
| us_tn_constitutions | 7 | 7 (100.00%) | 12 | 4,797 |
| us_tn_court_rules | 377 | 256 (67.90%) | 1,771 | 708,108 |
| us_tn_guidance | 169 | 118 (69.82%) | 327 | 130,675 |
| us_tn_statutes | 24,832 | 8,306 (33.45%) | 27,887 | 11,149,592 |
| us_tx_constitutions | 56 | 56 (100.00%) | 257 | 102,755 |
| us_tx_court_rules | 508 | 257 (50.59%) | 772 | 308,073 |
| us_tx_guidance | 1,246 | 852 (68.38%) | 2,549 | 1,018,763 |
| us_tx_regulations | 26,430 | 0 (0.00%) | 0 | 0 |
| us_tx_statutes | 37,685 | 2,195 (5.82%) | 3,135 | 1,253,469 |
| us_ut_constitutions | 10 | 10 (100.00%) | 18 | 7,191 |
| us_ut_court_rules | 749 | 512 (68.36%) | 1,584 | 633,355 |
| us_ut_guidance | 168 | 130 (77.38%) | 542 | 216,525 |
| us_ut_statutes | 0 | 0 (—) | 0 | 0 |
| us_va_constitutions | 14 | 12 (85.71%) | 19 | 7,594 |
| us_va_court_rules | 230 | 108 (46.96%) | 409 | 163,189 |
| us_va_guidance | 89 | 80 (89.89%) | 334 | 133,416 |
| us_va_regulations | 11,897 | 6,088 (51.17%) | 21,062 | 8,421,252 |
| us_va_statutes | 18,340 | 2,840 (15.49%) | 4,976 | 1,989,564 |
| us_vt_constitutions | 3 | 3 (100.00%) | 26 | 10,392 |
| us_vt_guidance | 184 | 140 (76.09%) | 544 | 217,400 |
| us_vt_statutes | 9,912 | 1,652 (16.67%) | 2,901 | 1,159,877 |
| us_wa_constitutions | 39 | 39 (100.00%) | 135 | 53,974 |
| us_wa_court_rules | 701 | 406 (57.92%) | 1,781 | 710,690 |
| us_wa_guidance | 24 | 23 (95.83%) | 106 | 42,346 |
| us_wa_regulations | 26,968 | 12,159 (45.09%) | 39,035 | 15,606,969 |
| us_wa_statutes | 3,875 | 3,311 (85.45%) | 5,037 | 2,013,699 |
| us_wi_constitutions | 22 | 21 (95.45%) | 57 | 22,787 |
| us_wi_court_rules | 233 | 139 (59.66%) | 578 | 230,649 |
| us_wi_guidance | 232 | 189 (81.47%) | 636 | 254,259 |
| us_wi_regulations | 10,808 | 5,772 (53.40%) | 15,781 | 6,309,807 |
| us_wi_statutes | 11,838 | 3,202 (27.05%) | 6,093 | 2,436,107 |
| us_wv_constitutions | 17 | 16 (94.12%) | 61 | 24,385 |
| us_wv_court_rules | 568 | 297 (52.29%) | 708 | 283,093 |
| us_wv_guidance | 173 | 157 (90.75%) | 1,207 | 482,425 |
| us_wv_statutes | 13,126 | 2,814 (21.44%) | 5,008 | 2,002,343 |
| us_wy_constitutions | 6 | 5 (83.33%) | 8 | 3,199 |
| us_wy_court_rules | 546 | 315 (57.69%) | 897 | 358,648 |
| us_wy_guidance | 62 | 45 (72.58%) | 128 | 51,160 |
| us_wy_statutes | 7,582 | 990 (13.06%) | 1,938 | 774,834 |

A file with **0 checkable rows** is not a clean file: it has no body carrying a newline at all, so the separator this detector requires is absent and its rate is **unknown**, not zero. Such a corpus can still be damaged in a form this producer cannot see. A `0.00%` against a large checkable count is the opposite — a positive result, and evidence the detector is not simply firing everywhere.

This is the dominant cause of COV-1A's 63,224 CFR text mismatches: the row states part of its own text twice, so nothing is missing and nothing is wrong — it is said again. Against the pinned eCFR edition the detector scores precision 1.0000 and recall 0.9980 on a balanced 993-section sample with **zero false positives**, which is what licenses reading the rates above for corpora that have no official oracle at all. `repeated characters` counts the surplus copies (a block appearing N times contributes N-1), and is an observation, not a claim about how much text a repair would remove.

Examples — us_ak_constitutions (smallest `act_id`s among the hits):

- `SCONST_AK_A10_S0` — 2 block(s), 800 repeated characters
- `SCONST_AK_A11_S0` — 1 block(s), 400 repeated characters
- `SCONST_AK_A12_S0` — 3 block(s), 1,200 repeated characters
- `SCONST_AK_A1_S0` — 4 block(s), 1,600 repeated characters
- `SCONST_AK_A2_S0` — 5 block(s), 1,999 repeated characters
- `SCONST_AK_A3_S0` — 4 block(s), 1,600 repeated characters
- `SCONST_AK_A4_S0` — 3 block(s), 1,200 repeated characters
- `SCONST_AK_A6_S0` — 3 block(s), 1,200 repeated characters

Examples — us_ak_court_rules (smallest `act_id`s among the hits):

- `SRULES_AK_ADMIN_R1` — 2 block(s), 798 repeated characters
- `SRULES_AK_ADMIN_R10` — 1 block(s), 400 repeated characters
- `SRULES_AK_ADMIN_R11` — 2 block(s), 799 repeated characters
- `SRULES_AK_ADMIN_R12` — 10 block(s), 3,989 repeated characters
- `SRULES_AK_ADMIN_R15` — 9 block(s), 3,590 repeated characters
- `SRULES_AK_ADMIN_R18` — 1 block(s), 399 repeated characters
- `SRULES_AK_ADMIN_R19_2` — 3 block(s), 1,196 repeated characters
- `SRULES_AK_ADMIN_R23` — 7 block(s), 2,796 repeated characters

Examples — us_ak_guidance (smallest `act_id`s among the hits):

- `AK_INS_B_1989-01` — 3 block(s), 1,199 repeated characters
- `AK_INS_B_1989-04` — 2 block(s), 800 repeated characters
- `AK_INS_B_1989-05` — 5 block(s), 1,997 repeated characters
- `AK_INS_B_1990-03` — 3 block(s), 1,197 repeated characters
- `AK_INS_B_1990-04` — 6 block(s), 2,386 repeated characters
- `AK_INS_B_1991-01` — 3 block(s), 1,198 repeated characters
- `AK_INS_B_1991-02` — 5 block(s), 1,997 repeated characters
- `AK_INS_B_1991-03` — 4 block(s), 1,598 repeated characters

Examples — us_ak_statutes (smallest `act_id`s among the hits):

- `STATE_AK_T10_C10.06_S10.06.210` — 1 block(s), 400 repeated characters
- `STATE_AK_T10_C10.06_S10.06.411` — 1 block(s), 400 repeated characters
- `STATE_AK_T10_C10.06_S10.06.420` — 1 block(s), 400 repeated characters
- `STATE_AK_T10_C10.06_S10.06.433` — 1 block(s), 399 repeated characters
- `STATE_AK_T10_C10.06_S10.06.435` — 1 block(s), 400 repeated characters
- `STATE_AK_T10_C10.06_S10.06.490` — 1 block(s), 400 repeated characters
- `STATE_AK_T10_C10.06_S10.06.576` — 1 block(s), 400 repeated characters
- `STATE_AK_T10_C10.06_S10.06.578` — 1 block(s), 400 repeated characters

Examples — us_al_constitutions (smallest `act_id`s among the hits):

- `SCONST_AL_AIII_S43.02` — 2 block(s), 798 repeated characters
- `SCONST_AL_AIV_S104` — 1 block(s), 399 repeated characters
- `SCONST_AL_AIV_S104.01` — 1 block(s), 400 repeated characters
- `SCONST_AL_AIV_S111.05` — 1 block(s), 400 repeated characters
- `SCONST_AL_AIV_S46` — 1 block(s), 400 repeated characters
- `SCONST_AL_AIV_S48.01` — 1 block(s), 400 repeated characters
- `SCONST_AL_AIV_S49` — 2 block(s), 799 repeated characters
- `SCONST_AL_AIV_S71.01` — 2 block(s), 800 repeated characters

Examples — us_al_court_rules (smallest `act_id`s among the hits):

- `SRULES_AL_ACJE_CANON1` — 1 block(s), 400 repeated characters
- `SRULES_AL_ACJE_CANON2` — 1 block(s), 400 repeated characters
- `SRULES_AL_ACJE_CANON3` — 15 block(s), 5,989 repeated characters
- `SRULES_AL_ACJE_CANON5` — 2 block(s), 797 repeated characters
- `SRULES_AL_ACJE_CANON6` — 2 block(s), 798 repeated characters
- `SRULES_AL_ACJE_CANON7` — 4 block(s), 1,595 repeated characters
- `SRULES_AL_ACJE_Dcancom` — 2 block(s), 798 repeated characters
- `SRULES_AL_ACSF_R2` — 2 block(s), 798 repeated characters

Examples — us_al_guidance (smallest `act_id`s among the hits):

- `AL_INS_B_2009-01` — 28 block(s), 11,196 repeated characters
- `AL_INS_B_2009-02` — 2 block(s), 799 repeated characters
- `AL_INS_B_2009-03` — 3 block(s), 1,200 repeated characters
- `AL_INS_B_2009-04` — 1 block(s), 400 repeated characters
- `AL_INS_B_2009-05` — 5 block(s), 2,000 repeated characters
- `AL_INS_B_2009-07_20090918` — 4 block(s), 1,599 repeated characters
- `AL_INS_B_2010-01` — 2 block(s), 800 repeated characters
- `AL_INS_B_2010-03` — 1 block(s), 400 repeated characters

Examples — us_al_statutes (smallest `act_id`s among the hits):

- `STATE_AL_T10A_C10_S10A-10-1.07` — 1 block(s), 400 repeated characters
- `STATE_AL_T10A_C10_S10A-10-1.15` — 2 block(s), 799 repeated characters
- `STATE_AL_T10A_C17_S10A-17-2.02` — 1 block(s), 399 repeated characters
- `STATE_AL_T10A_C1_S10A-1-1.03` — 7 block(s), 2,796 repeated characters
- `STATE_AL_T10A_C1_S10A-1-4.02` — 1 block(s), 399 repeated characters
- `STATE_AL_T10A_C1_S10A-1-4.31` — 1 block(s), 399 repeated characters
- `STATE_AL_T10A_C1_S10A-1-7.04` — 1 block(s), 400 repeated characters
- `STATE_AL_T10A_C1_S10A-1-8.01` — 4 block(s), 1,600 repeated characters

Examples — us_ar_constitutions (smallest `act_id`s among the hits):

- `SCONST_AR_A12_S4` — 1 block(s), 400 repeated characters
- `SCONST_AR_A14_S3` — 3 block(s), 1,199 repeated characters
- `SCONST_AR_A16_S14` — 5 block(s), 2,000 repeated characters
- `SCONST_AR_A18_S0` — 4 block(s), 1,599 repeated characters
- `SCONST_AR_A19_S28` — 6 block(s), 2,399 repeated characters
- `SCONST_AR_A19_S30` — 7 block(s), 2,799 repeated characters
- `SCONST_AR_A19_S31` — 6 block(s), 2,400 repeated characters
- `SCONST_AR_A5_S1` — 7 block(s), 2,799 repeated characters

Examples — us_ar_guidance (smallest `act_id`s among the hits):

- `AR_INS_B_1975-03` — 2 block(s), 799 repeated characters
- `AR_INS_B_1977-02` — 1 block(s), 400 repeated characters
- `AR_INS_B_1981-06` — 1 block(s), 399 repeated characters
- `AR_INS_B_1981-11` — 1 block(s), 399 repeated characters
- `AR_INS_B_1981-14` — 1 block(s), 399 repeated characters
- `AR_INS_B_1982-08` — 1 block(s), 398 repeated characters
- `AR_INS_B_1982-16` — 1 block(s), 399 repeated characters
- `AR_INS_B_1983-11` — 2 block(s), 800 repeated characters

Examples — us_ar_statutes (smallest `act_id`s among the hits):

- `STATE_AR_T10_C2_S1_S10-2-101` — 1 block(s), 400 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-112` — 1 block(s), 400 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-114` — 4 block(s), 1,600 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-120` — 1 block(s), 400 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-125` — 1 block(s), 400 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-127` — 2 block(s), 800 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-129` — 4 block(s), 1,600 repeated characters
- `STATE_AR_T10_C2_S1_S10-2-133` — 2 block(s), 800 repeated characters

Examples — us_az_constitutions (smallest `act_id`s among the hits):

- `SCONST_AZ_A10_S12` — 1 block(s), 400 repeated characters
- `SCONST_AZ_A10_S3` — 1 block(s), 400 repeated characters
- `SCONST_AZ_A10_S7` — 3 block(s), 1,200 repeated characters
- `SCONST_AZ_A11_S11` — 2 block(s), 800 repeated characters
- `SCONST_AZ_A12_S5` — 2 block(s), 800 repeated characters
- `SCONST_AZ_A12_S7` — 2 block(s), 799 repeated characters
- `SCONST_AZ_A12_S8` — 1 block(s), 400 repeated characters
- `SCONST_AZ_A13_S2` — 1 block(s), 400 repeated characters

Examples — us_az_court_rules (smallest `act_id`s among the hits):

- `SRULES_AZ_ARCAP_R10` — 4 block(s), 1,599 repeated characters
- `SRULES_AZ_ARCAP_R11` — 6 block(s), 2,398 repeated characters
- `SRULES_AZ_ARCAP_R11_1` — 2 block(s), 799 repeated characters
- `SRULES_AZ_ARCAP_R12` — 2 block(s), 799 repeated characters
- `SRULES_AZ_ARCAP_R13` — 4 block(s), 1,599 repeated characters
- `SRULES_AZ_ARCAP_R13_1` — 1 block(s), 399 repeated characters
- `SRULES_AZ_ARCAP_R15` — 3 block(s), 1,197 repeated characters
- `SRULES_AZ_ARCAP_R16` — 1 block(s), 400 repeated characters

Examples — us_az_guidance (smallest `act_id`s among the hits):

- `AZ_INS_CL_1981_02` — 2 block(s), 798 repeated characters
- `AZ_INS_CL_1981_03` — 3 block(s), 1,200 repeated characters
- `AZ_INS_CL_1985_02` — 1 block(s), 400 repeated characters
- `AZ_INS_CL_1987_06` — 2 block(s), 799 repeated characters
- `AZ_INS_CL_1988_01` — 1 block(s), 400 repeated characters
- `AZ_INS_CL_1989_02` — 1 block(s), 400 repeated characters
- `AZ_INS_CL_1990_01A` — 3 block(s), 1,199 repeated characters
- `AZ_INS_CL_1990_04A` — 5 block(s), 2,000 repeated characters

Examples — us_az_statutes (smallest `act_id`s among the hits):

- `STATE_AZ_T10_C11_A1_S1103` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C13_A1_S1302` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C14_A3_S1434` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C16_A2_S1622` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C19_A2_S2057` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C19_A2_S2077` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C19_A2_S2085` — 1 block(s), 400 repeated characters
- `STATE_AZ_T10_C19_A4_S2127` — 1 block(s), 400 repeated characters

Examples — us_ca_constitutions (smallest `act_id`s among the hits):

- `SCONST_CA_AIII_S6` — 2 block(s), 800 repeated characters
- `SCONST_CA_AIII_S8` — 4 block(s), 1,600 repeated characters
- `SCONST_CA_AII_S5` — 1 block(s), 400 repeated characters
- `SCONST_CA_AIV_S10` — 2 block(s), 800 repeated characters
- `SCONST_CA_AIV_S12` — 2 block(s), 799 repeated characters
- `SCONST_CA_AIV_S19` — 1 block(s), 400 repeated characters
- `SCONST_CA_AIV_S4` — 1 block(s), 400 repeated characters
- `SCONST_CA_AIV_S5` — 2 block(s), 799 repeated characters

Examples — us_ca_court_rules (smallest `act_id`s among the hits):

- `SRULES_CA_T10_R10_1` — 1 block(s), 400 repeated characters
- `SRULES_CA_T10_R10_10` — 1 block(s), 400 repeated characters
- `SRULES_CA_T10_R10_1004` — 2 block(s), 797 repeated characters
- `SRULES_CA_T10_R10_101` — 3 block(s), 1,200 repeated characters
- `SRULES_CA_T10_R10_1014` — 4 block(s), 1,599 repeated characters
- `SRULES_CA_T10_R10_1017` — 1 block(s), 400 repeated characters
- `SRULES_CA_T10_R10_1020` — 1 block(s), 398 repeated characters
- `SRULES_CA_T10_R10_1028` — 2 block(s), 799 repeated characters

Examples — us_ca_guidance (smallest `act_id`s among the hits):

- `CA_INS_B_1980-06` — 7 block(s), 2,798 repeated characters
- `CA_INS_B_1980-12` — 19 block(s), 7,595 repeated characters
- `CA_INS_B_1987-03` — 62 block(s), 24,734 repeated characters
- `CA_INS_B_1991-08` — 3 block(s), 1,198 repeated characters
- `CA_INS_B_1993-03` — 19 block(s), 7,590 repeated characters
- `CA_INS_B_1993-03A` — 22 block(s), 8,791 repeated characters
- `CA_INS_B_1993-04` — 8 block(s), 3,196 repeated characters
- `CA_INS_B_1993-04A` — 9 block(s), 3,597 repeated characters

Examples — us_ca_statutes (smallest `act_id`s among the hits):

- `STATE_CA_Cbpc_AGENERAL PROVISIONS_S27` — 1 block(s), 400 repeated characters
- `STATE_CA_Cbpc_AGENERAL PROVISIONS_S27.5` — 1 block(s), 400 repeated characters
- `STATE_CA_Cbpc_AGENERAL PROVISIONS_S30` — 2 block(s), 800 repeated characters
- `STATE_CA_Cbpc_D1.5_C2_S480` — 2 block(s), 798 repeated characters
- `STATE_CA_Cbpc_D1.5_C2_S480.2` — 1 block(s), 400 repeated characters
- `STATE_CA_Cbpc_D1.5_C3_S494` — 2 block(s), 800 repeated characters
- `STATE_CA_Cbpc_D1.5_C3_S494.5` — 6 block(s), 2,399 repeated characters
- `STATE_CA_Cbpc_D10_C10_S26100` — 1 block(s), 399 repeated characters

Examples — us_co_constitutions (smallest `act_id`s among the hits):

- `SCONST_CO_AII_S15` — 1 block(s), 399 repeated characters
- `SCONST_CO_AII_S16` — 1 block(s), 400 repeated characters
- `SCONST_CO_AII_S19` — 2 block(s), 799 repeated characters
- `SCONST_CO_AIX_S10` — 1 block(s), 400 repeated characters
- `SCONST_CO_AIX_S17` — 1 block(s), 399 repeated characters
- `SCONST_CO_AVI_S10` — 1 block(s), 400 repeated characters
- `SCONST_CO_AVI_S20` — 1 block(s), 400 repeated characters
- `SCONST_CO_AVI_S23` — 10 block(s), 4,000 repeated characters

Examples — us_co_regulations (smallest `act_id`s among the hits):

- `STATE_CO_CCR_10_CCR_2505_5` — 156 block(s), 62,371 repeated characters
- `STATE_CO_CCR_10_CCR_2506_1` — 464 block(s), 185,537 repeated characters
- `STATE_CO_CCR_11_CCR_2508_1` — 17 block(s), 6,795 repeated characters
- `STATE_CO_CCR_12_CCR_2512_2` — 50 block(s), 19,995 repeated characters
- `STATE_CO_CCR_12_CCR_2515_1` — 2 block(s), 800 repeated characters
- `STATE_CO_CCR_12_CCR_2516_1` — 48 block(s), 19,190 repeated characters
- `STATE_CO_CCR_1_CCR_101_1` — 175 block(s), 69,977 repeated characters
- `STATE_CO_CCR_1_CCR_101_9` — 86 block(s), 34,385 repeated characters

Examples — us_co_statutes (smallest `act_id`s among the hits):

- `STATE_CO_T10_A10_S10-10-109` — 2 block(s), 800 repeated characters
- `STATE_CO_T10_A11_P1_S10-11-102` — 2 block(s), 800 repeated characters
- `STATE_CO_T10_A11_P2_S10-11-201` — 1 block(s), 400 repeated characters
- `STATE_CO_T10_A12_P1_S10-12-101` — 1 block(s), 400 repeated characters
- `STATE_CO_T10_A12_P4_S10-12-411` — 1 block(s), 400 repeated characters
- `STATE_CO_T10_A14_P3_S10-14-301` — 1 block(s), 400 repeated characters
- `STATE_CO_T10_A14_P4_S10-14-404` — 1 block(s), 400 repeated characters
- `STATE_CO_T10_A15_S10-15-102` — 1 block(s), 400 repeated characters

Examples — us_ct_constitutions (smallest `act_id`s among the hits):

- `SCONST_CT_AAMENDIII_S0` — 1 block(s), 400 repeated characters
- `SCONST_CT_AAMENDXII_S0` — 3 block(s), 1,199 repeated characters
- `SCONST_CT_AAMENDXVI_S2` — 3 block(s), 1,198 repeated characters
- `SCONST_CT_AAMENDXXII_S0` — 3 block(s), 1,199 repeated characters
- `SCONST_CT_AAMENDXXIX_S0` — 1 block(s), 400 repeated characters
- `SCONST_CT_AAMENDXXVI_S0` — 3 block(s), 1,198 repeated characters
- `SCONST_CT_AAMENDXXXIV_S4` — 1 block(s), 400 repeated characters
- `SCONST_CT_AAMENDXXX_S2` — 1 block(s), 399 repeated characters

Examples — us_ct_court_rules (smallest `act_id`s among the hits):

- `SRULES_CT_EVID_R10_1` — 2 block(s), 800 repeated characters
- `SRULES_CT_EVID_R10_3` — 2 block(s), 800 repeated characters
- `SRULES_CT_EVID_R10_6` — 5 block(s), 1,999 repeated characters
- `SRULES_CT_EVID_R1_1` — 5 block(s), 1,998 repeated characters
- `SRULES_CT_EVID_R1_2` — 2 block(s), 800 repeated characters
- `SRULES_CT_EVID_R1_3` — 3 block(s), 1,199 repeated characters
- `SRULES_CT_EVID_R1_5` — 1 block(s), 400 repeated characters
- `SRULES_CT_EVID_R2_1` — 2 block(s), 799 repeated characters

Examples — us_ct_guidance (smallest `act_id`s among the hits):

- `CT_INS_CL_1_07` — 2 block(s), 799 repeated characters
- `CT_INS_CL_4` — 1 block(s), 400 repeated characters
- `CT_INS_CL_5` — 6 block(s), 2,400 repeated characters
- `CT_INS_C_3` — 10 block(s), 3,998 repeated characters
- `CT_INS_FS_14C_00` — 9 block(s), 3,595 repeated characters
- `CT_INS_FS_16_07` — 1 block(s), 400 repeated characters
- `CT_INS_FS_16_08` — 2 block(s), 797 repeated characters
- `CT_INS_FS_16_15` — 1 block(s), 400 repeated characters

Examples — us_ct_statutes (smallest `act_id`s among the hits):

- `STATE_CT_T10_C163_S10-10a` — 2 block(s), 799 repeated characters
- `STATE_CT_T10_C163_S10-4v` — 1 block(s), 399 repeated characters
- `STATE_CT_T10_C163_S10-4w` — 1 block(s), 400 repeated characters
- `STATE_CT_T10_C163c_S10-14u` — 3 block(s), 1,200 repeated characters
- `STATE_CT_T10_C164_S10-15f` — 12 block(s), 4,799 repeated characters
- `STATE_CT_T10_C164_S10-15j` — 1 block(s), 400 repeated characters
- `STATE_CT_T10_C164_S10-16b` — 2 block(s), 800 repeated characters
- `STATE_CT_T10_C164_S10-16p` — 8 block(s), 3,196 repeated characters

Examples — us_dc_court_rules (smallest `act_id`s among the hits):

- `SRULES_DC_DCCA_R1` — 1 block(s), 399 repeated characters
- `SRULES_DC_DCCA_R10` — 2 block(s), 798 repeated characters
- `SRULES_DC_DCCA_R11` — 1 block(s), 399 repeated characters
- `SRULES_DC_DCCA_R15` — 2 block(s), 798 repeated characters
- `SRULES_DC_DCCA_R21` — 1 block(s), 399 repeated characters
- `SRULES_DC_DCCA_R24` — 4 block(s), 1,596 repeated characters
- `SRULES_DC_DCCA_R25` — 4 block(s), 1,597 repeated characters
- `SRULES_DC_DCCA_R25_1` — 3 block(s), 1,197 repeated characters

Examples — us_dc_guidance (smallest `act_id`s among the hits):

- `DC_INS_B_20_6_IB_08_24` — 1 block(s), 400 repeated characters
- `DC_INS_B_24_IB_002_05_21` — 17 block(s), 6,796 repeated characters
- `DC_INS_B_24_IB_003_05_28` — 9 block(s), 3,598 repeated characters
- `DC_INS_B_24_IB_003_05_31` — 1 block(s), 400 repeated characters
- `DC_INS_B_25_IB_001_08_12` — 1 block(s), 400 repeated characters
- `DC_INS_B_25_IB_003_09_17` — 2 block(s), 800 repeated characters
- `DC_INS_B_26_IB_001_1_6` — 4 block(s), 1,598 repeated characters
- `DC_INS_B_Bulletin15_IB_06_8_15` — 2 block(s), 800 repeated characters

Examples — us_dc_statutes (smallest `act_id`s among the hits):

- `STATE_DC_T10_C10A_S10-1031` — 2 block(s), 799 repeated characters
- `STATE_DC_T10_C10B_S10-1052` — 3 block(s), 1,200 repeated characters
- `STATE_DC_T10_C10B_S10-1053.01` — 1 block(s), 400 repeated characters
- `STATE_DC_T10_C11A_S10-1181.02` — 1 block(s), 399 repeated characters
- `STATE_DC_T10_C11_S10-1101.01` — 2 block(s), 800 repeated characters
- `STATE_DC_T10_C11_S10-1102.01` — 1 block(s), 399 repeated characters
- `STATE_DC_T10_C11_S10-1102.01a` — 1 block(s), 399 repeated characters
- `STATE_DC_T10_C11_S10-1102.02` — 1 block(s), 400 repeated characters

Examples — us_de_constitutions (smallest `act_id`s among the hits):

- `SCONST_DE_AIII_S10` — 1 block(s), 400 repeated characters
- `SCONST_DE_AIII_S18` — 1 block(s), 400 repeated characters
- `SCONST_DE_AIII_S20` — 2 block(s), 799 repeated characters
- `SCONST_DE_AII_S17A` — 1 block(s), 400 repeated characters
- `SCONST_DE_AII_S17B` — 1 block(s), 400 repeated characters
- `SCONST_DE_AII_S2` — 8 block(s), 3,199 repeated characters
- `SCONST_DE_AII_S2A` — 1 block(s), 400 repeated characters
- `SCONST_DE_AIV_S11` — 2 block(s), 799 repeated characters

Examples — us_de_court_rules (smallest `act_id`s among the hits):

- `SRULES_DE_DECCPCIV_R107` — 3 block(s), 1,196 repeated characters
- `SRULES_DE_DECCPCIV_R11` — 2 block(s), 797 repeated characters
- `SRULES_DE_DECCPCIV_R112` — 2 block(s), 797 repeated characters
- `SRULES_DE_DECCPCIV_R12` — 1 block(s), 399 repeated characters
- `SRULES_DE_DECCPCIV_R13` — 1 block(s), 399 repeated characters
- `SRULES_DE_DECCPCIV_R14` — 1 block(s), 399 repeated characters
- `SRULES_DE_DECCPCIV_R15` — 1 block(s), 398 repeated characters
- `SRULES_DE_DECCPCIV_R16` — 6 block(s), 2,393 repeated characters

Examples — us_de_guidance (smallest `act_id`s among the hits):

- `DE_INS_AUTO_10_19981015` — 1 block(s), 399 repeated characters
- `DE_INS_AUTO_1_20180125` — 3 block(s), 1,200 repeated characters
- `DE_INS_AUTO_23_20151006` — 1 block(s), 400 repeated characters
- `DE_INS_AUTO_25_20180815` — 3 block(s), 1,199 repeated characters
- `DE_INS_AUTO_27_20170807` — 2 block(s), 800 repeated characters
- `DE_INS_AUTO_28_20170915` — 1 block(s), 400 repeated characters
- `DE_INS_AUTO_29_20180501` — 5 block(s), 1,999 repeated characters
- `DE_INS_AUTO_30_20181026` — 1 block(s), 400 repeated characters

Examples — us_de_regulations (smallest `act_id`s among the hits):

- `STATE_DE_ADC_T10_101` — 19 block(s), 7,597 repeated characters
- `STATE_DE_ADC_T10_102` — 9 block(s), 3,598 repeated characters
- `STATE_DE_ADC_T10_103` — 24 block(s), 9,593 repeated characters
- `STATE_DE_ADC_T10_104` — 5 block(s), 2,000 repeated characters
- `STATE_DE_ADC_T10_201` — 15 block(s), 5,997 repeated characters
- `STATE_DE_ADC_T10_202` — 39 block(s), 15,593 repeated characters
- `STATE_DE_ADC_T10_203` — 168 block(s), 67,173 repeated characters
- `STATE_DE_ADC_T10_204` — 44 block(s), 17,595 repeated characters

Examples — us_de_statutes (smallest `act_id`s among the hits):

- `STATE_DE_T10_C23_S2306` — 1 block(s), 400 repeated characters
- `STATE_DE_T10_C31_S3104` — 1 block(s), 399 repeated characters
- `STATE_DE_T10_C31_S3114` — 1 block(s), 400 repeated characters
- `STATE_DE_T10_C39_S3930` — 1 block(s), 400 repeated characters
- `STATE_DE_T10_C43_SI_S4319` — 1 block(s), 400 repeated characters
- `STATE_DE_T10_C47_SI_S4711` — 1 block(s), 400 repeated characters
- `STATE_DE_T10_C49_SXI_S5062B` — 1 block(s), 399 repeated characters
- `STATE_DE_T10_C49_SXI_S5062C` — 8 block(s), 3,199 repeated characters

Examples — us_federal_enforcement_action (smallest `act_id`s among the hits):

- `HHS_OCR_RESOLUTION_2018ENFORCEMENT` — 4 block(s), 1,599 repeated characters
- `HHS_OCR_RESOLUTION_CATHOLIC_HEALTH_CARE_SERVICES` — 1 block(s), 400 repeated characters
- `HHS_OCR_RESOLUTION_CIGNETCMP` — 1 block(s), 400 repeated characters
- `HHS_OCR_RESOLUTION_CVSRESOLUTIONAGREEMENT` — 2 block(s), 800 repeated characters
- `HHS_OCR_RESOLUTION_DISPOSALFAQS` — 8 block(s), 3,198 repeated characters
- `HHS_OCR_RESOLUTION_DMS_RA_CAP` — 16 block(s), 6,398 repeated characters
- `HHS_OCR_RESOLUTION_FACT_SHEET_42_CFR_PART_2_FINAL_RULE` — 4 block(s), 1,599 repeated characters
- `HHS_OCR_RESOLUTION_GREEN_RIDGE_BEHAVIORAL_HEALTH_RA_CAP` — 19 block(s), 7,595 repeated characters

Examples — us_federal_executive_order (smallest `act_id`s among the hits):

- `EXEC_2015-00058` — 5 block(s), 1,995 repeated characters
- `EXEC_2015-01255` — 5 block(s), 2,000 repeated characters
- `EXEC_2015-01522` — 9 block(s), 3,591 repeated characters
- `EXEC_2015-02379` — 8 block(s), 3,198 repeated characters
- `EXEC_2015-03714` — 9 block(s), 3,590 repeated characters
- `EXEC_2015-05677` — 9 block(s), 3,600 repeated characters
- `EXEC_2015-07016` — 39 block(s), 15,585 repeated characters
- `EXEC_2015-07788` — 5 block(s), 1,998 repeated characters

Examples — us_federal_faq (smallest `act_id`s among the hits):

- `HHS_OCR_HIPAA_FAQ_1065` — 1 block(s), 399 repeated characters
- `HHS_OCR_HIPAA_FAQ_1067` — 1 block(s), 400 repeated characters
- `HHS_OCR_HIPAA_FAQ_1068` — 1 block(s), 399 repeated characters
- `HHS_OCR_HIPAA_FAQ_189` — 1 block(s), 400 repeated characters
- `HHS_OCR_HIPAA_FAQ_193` — 1 block(s), 400 repeated characters
- `HHS_OCR_HIPAA_FAQ_196` — 1 block(s), 400 repeated characters
- `HHS_OCR_HIPAA_FAQ_197` — 1 block(s), 400 repeated characters
- `HHS_OCR_HIPAA_FAQ_200` — 1 block(s), 400 repeated characters

Examples — us_federal_guidance (smallest `act_id`s among the hits):

- `BIS_AO_20030515` — 3 block(s), 1,199 repeated characters
- `BIS_AO_20031003` — 1 block(s), 399 repeated characters
- `BIS_AO_20040527` — 1 block(s), 400 repeated characters
- `BIS_AO_20040826` — 3 block(s), 1,198 repeated characters
- `BIS_AO_20041206` — 2 block(s), 800 repeated characters
- `BIS_AO_20060111` — 7 block(s), 2,799 repeated characters
- `BIS_AO_20060605` — 4 block(s), 1,600 repeated characters
- `BIS_AO_20070802` — 5 block(s), 1,999 repeated characters

Examples — us_federal_guideline (smallest `act_id`s among the hits):

- `USSG_S1A1.1` — 4 block(s), 1,600 repeated characters
- `USSG_S1B1.1` — 8 block(s), 3,200 repeated characters
- `USSG_S1B1.10` — 14 block(s), 5,595 repeated characters
- `USSG_S1B1.11` — 5 block(s), 2,000 repeated characters
- `USSG_S1B1.13` — 5 block(s), 1,999 repeated characters
- `USSG_S1B1.2` — 6 block(s), 2,398 repeated characters
- `USSG_S1B1.3` — 24 block(s), 9,596 repeated characters
- `USSG_S1B1.5` — 2 block(s), 799 repeated characters

Examples — us_federal_irs_announcement (smallest `act_id`s among the hits):

- `IRS_ANN_2015_1` — 2 block(s), 800 repeated characters
- `IRS_ANN_2015_11` — 31 block(s), 12,393 repeated characters
- `IRS_ANN_2015_13` — 3 block(s), 1,200 repeated characters
- `IRS_ANN_2015_19` — 5 block(s), 1,996 repeated characters
- `IRS_ANN_2015_2` — 10 block(s), 3,997 repeated characters
- `IRS_ANN_2015_22` — 2 block(s), 800 repeated characters
- `IRS_ANN_2015_3` — 6 block(s), 2,397 repeated characters
- `IRS_ANN_2015_8` — 3 block(s), 1,199 repeated characters

Examples — us_federal_irs_notice (smallest `act_id`s among the hits):

- `IRS_NOTICE_2015_10` — 11 block(s), 4,399 repeated characters
- `IRS_NOTICE_2015_11` — 6 block(s), 2,398 repeated characters
- `IRS_NOTICE_2015_12` — 47 block(s), 18,777 repeated characters
- `IRS_NOTICE_2015_13` — 2 block(s), 799 repeated characters
- `IRS_NOTICE_2015_14` — 30 block(s), 11,991 repeated characters
- `IRS_NOTICE_2015_15` — 15 block(s), 5,990 repeated characters
- `IRS_NOTICE_2015_16` — 49 block(s), 19,582 repeated characters
- `IRS_NOTICE_2015_17` — 13 block(s), 5,197 repeated characters

Examples — us_federal_irs_rev_proc (smallest `act_id`s among the hits):

- `IRS_RP_2015_12` — 41 block(s), 16,355 repeated characters
- `IRS_RP_2015_13` — 140 block(s), 55,876 repeated characters
- `IRS_RP_2015_14` — 500 block(s), 199,274 repeated characters
- `IRS_RP_2015_15` — 2 block(s), 799 repeated characters
- `IRS_RP_2015_17` — 7 block(s), 2,795 repeated characters
- `IRS_RP_2015_19` — 13 block(s), 5,193 repeated characters
- `IRS_RP_2015_20` — 18 block(s), 7,190 repeated characters
- `IRS_RP_2015_21` — 16 block(s), 6,389 repeated characters

Examples — us_federal_irs_rev_rul (smallest `act_id`s among the hits):

- `IRS_RR_2015_1` — 2 block(s), 797 repeated characters
- `IRS_RR_2015_10` — 7 block(s), 2,797 repeated characters
- `IRS_RR_2015_11` — 7 block(s), 2,797 repeated characters
- `IRS_RR_2015_12` — 20 block(s), 7,986 repeated characters
- `IRS_RR_2015_13` — 5 block(s), 1,998 repeated characters
- `IRS_RR_2015_14` — 1 block(s), 400 repeated characters
- `IRS_RR_2015_15` — 2 block(s), 800 repeated characters
- `IRS_RR_2015_16` — 1 block(s), 400 repeated characters

Examples — us_federal_memorandum (smallest `act_id`s among the hits):

- `EXEC_2015-01118` — 6 block(s), 2,398 repeated characters
- `EXEC_2015-01256` — 5 block(s), 1,994 repeated characters
- `EXEC_2015-03727` — 11 block(s), 4,399 repeated characters
- `EXEC_2015-04443` — 12 block(s), 4,800 repeated characters
- `EXEC_2015-05933` — 12 block(s), 4,794 repeated characters
- `EXEC_2015-06383` — 2 block(s), 799 repeated characters
- `EXEC_2015-08685` — 1 block(s), 395 repeated characters
- `EXEC_2015-10501` — 1 block(s), 400 repeated characters

Examples — us_federal_presidential_document (smallest `act_id`s among the hits):

- `EXEC_2015-01283` — 1 block(s), 400 repeated characters
- `EXEC_2015-02603` — 2 block(s), 800 repeated characters
- `EXEC_2015-04091` — 1 block(s), 400 repeated characters
- `EXEC_2015-04353` — 1 block(s), 400 repeated characters
- `EXEC_2015-05337` — 1 block(s), 400 repeated characters
- `EXEC_2015-05338` — 2 block(s), 800 repeated characters
- `EXEC_2015-06031` — 2 block(s), 800 repeated characters
- `EXEC_2015-07786` — 1 block(s), 400 repeated characters

Examples — us_federal_proclamation (smallest `act_id`s among the hits):

- `EXEC_2015-00068` — 2 block(s), 799 repeated characters
- `EXEC_2015-00073` — 2 block(s), 800 repeated characters
- `EXEC_2015-00077` — 2 block(s), 800 repeated characters
- `EXEC_2015-01112` — 3 block(s), 1,200 repeated characters
- `EXEC_2015-01254` — 3 block(s), 1,200 repeated characters
- `EXEC_2015-02372` — 3 block(s), 1,200 repeated characters
- `EXEC_2015-02374` — 1 block(s), 398 repeated characters
- `EXEC_2015-02377` — 4 block(s), 1,600 repeated characters

Examples — us_federal_regulations (smallest `act_id`s among the hits):

- `CFR_T10_P1002_S1002_12` — 1 block(s), 400 repeated characters
- `CFR_T10_P1003_S1003_12` — 1 block(s), 400 repeated characters
- `CFR_T10_P1003_S1003_14` — 1 block(s), 400 repeated characters
- `CFR_T10_P1003_S1003_15` — 3 block(s), 1,200 repeated characters
- `CFR_T10_P1003_S1003_16` — 1 block(s), 400 repeated characters
- `CFR_T10_P1003_S1003_2` — 2 block(s), 800 repeated characters
- `CFR_T10_P1003_S1003_7` — 2 block(s), 800 repeated characters
- `CFR_T10_P1004_S1004_10` — 2 block(s), 800 repeated characters

Examples — us_federal_ruling (smallest `act_id`s among the hits):

- `FCC_DA_00_1341` — 9 block(s), 3,598 repeated characters
- `FCC_DA_01_2234` — 9 block(s), 3,588 repeated characters
- `FCC_DA_01_2871` — 6 block(s), 2,393 repeated characters
- `FCC_DA_02_2078` — 1 block(s), 400 repeated characters
- `FCC_DA_02_765` — 70 block(s), 27,923 repeated characters
- `FCC_DA_03_2865` — 4 block(s), 1,599 repeated characters
- `FCC_DA_03_4108` — 16 block(s), 6,389 repeated characters
- `FCC_DA_04_3201` — 5 block(s), 1,995 repeated characters

Examples — us_federal_statutes (smallest `act_id`s among the hits):

- `USC_T10_C1001_S10001` — 3 block(s), 1,200 repeated characters
- `USC_T10_C1003_S10101` — 23 block(s), 9,198 repeated characters
- `USC_T10_C1003_S10105` — 7 block(s), 2,800 repeated characters
- `USC_T10_C1005_S10145` — 1 block(s), 400 repeated characters
- `USC_T10_C1005_S10147` — 1 block(s), 400 repeated characters
- `USC_T10_C1005_S10148` — 1 block(s), 400 repeated characters
- `USC_T10_C1005_S10149` — 2 block(s), 800 repeated characters
- `USC_T10_C1005_S10154` — 2 block(s), 799 repeated characters

Examples — us_federal_treaty (smallest `act_id`s among the hits):

- `TREATY_US_ARMENIA` — 25 block(s), 9,997 repeated characters
- `TREATY_US_AUSTRALIA` — 48 block(s), 19,195 repeated characters
- `TREATY_US_AUSTRALIA_TE` — 56 block(s), 22,391 repeated characters
- `TREATY_US_AUSTRIA` — 81 block(s), 32,373 repeated characters
- `TREATY_US_AUSTRIA_TE` — 158 block(s), 63,102 repeated characters
- `TREATY_US_AZERBAIJAN` — 25 block(s), 9,997 repeated characters
- `TREATY_US_BANGLADESH` — 46 block(s), 18,369 repeated characters
- `TREATY_US_BANGLADESH_TE` — 177 block(s), 70,730 repeated characters

Examples — us_fl_constitutions (smallest `act_id`s among the hits):

- `SCONST_FL_AIII_S16` — 1 block(s), 400 repeated characters
- `SCONST_FL_AIII_S19` — 7 block(s), 2,800 repeated characters
- `SCONST_FL_AIII_S3` — 1 block(s), 399 repeated characters
- `SCONST_FL_AIII_S4` — 1 block(s), 400 repeated characters
- `SCONST_FL_AIII_S8` — 1 block(s), 400 repeated characters
- `SCONST_FL_AII_S1` — 1 block(s), 398 repeated characters
- `SCONST_FL_AII_S8` — 4 block(s), 1,600 repeated characters
- `SCONST_FL_AIV_S1` — 1 block(s), 399 repeated characters

Examples — us_fl_court_rules (smallest `act_id`s among the hits):

- `SRULES_FL_APPELLATE_R3_800` — 1 block(s), 400 repeated characters
- `SRULES_FL_APPELLATE_R9_010` — 1 block(s), 400 repeated characters
- `SRULES_FL_APPELLATE_R9_020` — 10 block(s), 3,999 repeated characters
- `SRULES_FL_APPELLATE_R9_030` — 10 block(s), 3,996 repeated characters
- `SRULES_FL_APPELLATE_R9_040` — 7 block(s), 2,798 repeated characters
- `SRULES_FL_APPELLATE_R9_100` — 17 block(s), 6,799 repeated characters
- `SRULES_FL_APPELLATE_R9_110` — 14 block(s), 5,598 repeated characters
- `SRULES_FL_APPELLATE_R9_120` — 6 block(s), 2,400 repeated characters

Examples — us_fl_guidance (smallest `act_id`s among the hits):

- `FL_OIR_OIR_14_01M` — 1 block(s), 400 repeated characters
- `FL_OIR_OIR_14_02M` — 1 block(s), 400 repeated characters
- `FL_OIR_OIR_14_04M` — 2 block(s), 800 repeated characters
- `FL_OIR_OIR_14_05M` — 4 block(s), 1,599 repeated characters
- `FL_OIR_OIR_15_01M` — 1 block(s), 400 repeated characters
- `FL_OIR_OIR_15_02M` — 8 block(s), 3,193 repeated characters
- `FL_OIR_OIR_15_04M` — 2 block(s), 799 repeated characters
- `FL_OIR_OIR_15_05M` — 2 block(s), 798 repeated characters

Examples — us_fl_statutes (smallest `act_id`s among the hits):

- `STATE_FL_TIII_C10_S10.202` — 107 block(s), 42,770 repeated characters
- `STATE_FL_TIII_C10_S10.203` — 41 block(s), 16,394 repeated characters
- `STATE_FL_TIII_C11_S11.0431` — 1 block(s), 400 repeated characters
- `STATE_FL_TIII_C11_S11.045` — 4 block(s), 1,599 repeated characters
- `STATE_FL_TIII_C11_S11.13` — 1 block(s), 400 repeated characters
- `STATE_FL_TIII_C11_S11.143` — 1 block(s), 400 repeated characters
- `STATE_FL_TIII_C11_S11.242` — 2 block(s), 800 repeated characters
- `STATE_FL_TIII_C11_S11.40` — 2 block(s), 800 repeated characters

Examples — us_ga_constitutions (smallest `act_id`s among the hits):

- `SCONST_GA_AI.II_SIX` — 1 block(s), 400 repeated characters
- `SCONST_GA_AI.II_SV` — 1 block(s), 400 repeated characters
- `SCONST_GA_AI.II_SVIII` — 2 block(s), 799 repeated characters
- `SCONST_GA_AI.I_SXXX` — 1 block(s), 400 repeated characters
- `SCONST_GA_AII.III_SI` — 3 block(s), 1,200 repeated characters
- `SCONST_GA_AIII.IX_SVI` — 13 block(s), 5,196 repeated characters
- `SCONST_GA_AIII.VI_SII` — 1 block(s), 400 repeated characters
- `SCONST_GA_AIII.VI_SV` — 1 block(s), 400 repeated characters

Examples — us_ga_court_rules (smallest `act_id`s among the hits):

- `SRULES_GA_CJC_R1_2` — 1 block(s), 400 repeated characters
- `SRULES_GA_CJC_R1_3` — 1 block(s), 400 repeated characters
- `SRULES_GA_CJC_R2_11` — 3 block(s), 1,197 repeated characters
- `SRULES_GA_CJC_R2_15` — 1 block(s), 400 repeated characters
- `SRULES_GA_CJC_R2_3` — 1 block(s), 400 repeated characters
- `SRULES_GA_CJC_R2_5` — 2 block(s), 800 repeated characters
- `SRULES_GA_CJC_R2_9` — 4 block(s), 1,598 repeated characters
- `SRULES_GA_CJC_R3_11` — 1 block(s), 399 repeated characters

Examples — us_ga_guidance (smallest `act_id`s among the hits):

- `GA_INS_B_2020_EX_02` — 2 block(s), 800 repeated characters
- `GA_INS_B_2020_EX_03` — 2 block(s), 800 repeated characters
- `GA_INS_B_2020_EX_04` — 1 block(s), 400 repeated characters
- `GA_INS_B_2020_EX_09` — 1 block(s), 400 repeated characters
- `GA_INS_B_2020_EX_10` — 1 block(s), 400 repeated characters
- `GA_INS_B_2021_EX_05` — 1 block(s), 399 repeated characters
- `GA_INS_B_2021_EX_06` — 2 block(s), 799 repeated characters
- `GA_INS_B_2021_EX_07` — 1 block(s), 400 repeated characters

Examples — us_hi_constitutions (smallest `act_id`s among the hits):

- `SCONST_HI_AIII_S16` — 1 block(s), 400 repeated characters
- `SCONST_HI_AVII_S12` — 3 block(s), 1,200 repeated characters
- `SCONST_HI_AVII_S13` — 4 block(s), 1,600 repeated characters
- `SCONST_HI_AVII_S9` — 1 block(s), 399 repeated characters
- `SCONST_HI_AVI_S3` — 2 block(s), 800 repeated characters
- `SCONST_HI_AVI_S4` — 1 block(s), 400 repeated characters
- `SCONST_HI_AV_S6` — 1 block(s), 400 repeated characters
- `SCONST_HI_AXII_S1` — 1 block(s), 400 repeated characters

Examples — us_hi_court_rules (smallest `act_id`s among the hits):

- `SRULES_HI_CSLI_R17` — 9 block(s), 3,599 repeated characters
- `SRULES_HI_CSLI_R9` — 1 block(s), 400 repeated characters
- `SRULES_HI_DCRCP_R11_1` — 2 block(s), 800 repeated characters
- `SRULES_HI_DCRCP_R11_SIGNING` — 1 block(s), 400 repeated characters
- `SRULES_HI_DCRCP_R12` — 3 block(s), 1,200 repeated characters
- `SRULES_HI_DCRCP_R13` — 1 block(s), 400 repeated characters
- `SRULES_HI_DCRCP_R14` — 1 block(s), 400 repeated characters
- `SRULES_HI_DCRCP_R15_AMENDED` — 1 block(s), 400 repeated characters

Examples — us_hi_guidance (smallest `act_id`s among the hits):

- `HI_INS_CM_2002-10R` — 3 block(s), 1,193 repeated characters
- `HI_INS_CM_2002-11E` — 9 block(s), 3,593 repeated characters
- `HI_INS_CM_2002-12E` — 9 block(s), 3,598 repeated characters
- `HI_INS_CM_2002-13H` — 8 block(s), 3,195 repeated characters
- `HI_INS_CM_2002-14E` — 1 block(s), 400 repeated characters
- `HI_INS_CM_2002-15E` — 7 block(s), 2,799 repeated characters
- `HI_INS_CM_2002-16C` — 4 block(s), 1,597 repeated characters
- `HI_INS_CM_2002-17R` — 19 block(s), 7,594 repeated characters

Examples — us_hi_statutes (smallest `act_id`s among the hits):

- `STATE_HI_D1_T10_C127A_S127A-12` — 4 block(s), 1,600 repeated characters
- `STATE_HI_D1_T10_C127A_S127A-13` — 2 block(s), 800 repeated characters
- `STATE_HI_D1_T10_C127A_S127A-16` — 1 block(s), 400 repeated characters
- `STATE_HI_D1_T10_C127A_S127A-2` — 1 block(s), 400 repeated characters
- `STATE_HI_D1_T10_C127A_S127A-3` — 1 block(s), 400 repeated characters
- `STATE_HI_D1_T10_C127A_S127A-30` — 1 block(s), 400 repeated characters
- `STATE_HI_D1_T10_C128D_S128D-17` — 1 block(s), 399 repeated characters
- `STATE_HI_D1_T10_C128D_S128D-18` — 1 block(s), 400 repeated characters

Examples — us_ia_constitutions (smallest `act_id`s among the hits):

- `SCONST_IA_AIII_S16` — 1 block(s), 400 repeated characters
- `SCONST_IA_AV_S16` — 1 block(s), 400 repeated characters

Examples — us_ia_court_rules (smallest `act_id`s among the hits):

- `SRULES_IA_CH11_R11_10` — 1 block(s), 400 repeated characters
- `SRULES_IA_CH11_R11_4` — 1 block(s), 399 repeated characters
- `SRULES_IA_CH11_R11_7` — 1 block(s), 400 repeated characters
- `SRULES_IA_CH15_R15_302` — 2 block(s), 799 repeated characters
- `SRULES_IA_CH16_R16_201` — 11 block(s), 4,398 repeated characters
- `SRULES_IA_CH16_R16_303` — 1 block(s), 400 repeated characters
- `SRULES_IA_CH16_R16_304` — 6 block(s), 2,400 repeated characters
- `SRULES_IA_CH16_R16_305` — 1 block(s), 400 repeated characters

Examples — us_ia_guidance (smallest `act_id`s among the hits):

- `IA_INS_B_00_04` — 1 block(s), 400 repeated characters
- `IA_INS_B_04_01` — 1 block(s), 400 repeated characters
- `IA_INS_B_06_01` — 2 block(s), 800 repeated characters
- `IA_INS_B_07_02` — 1 block(s), 400 repeated characters
- `IA_INS_B_07_03` — 2 block(s), 800 repeated characters
- `IA_INS_B_07_04` — 1 block(s), 400 repeated characters
- `IA_INS_B_07_05` — 2 block(s), 798 repeated characters
- `IA_INS_B_08_13` — 10 block(s), 3,993 repeated characters

Examples — us_ia_statutes (smallest `act_id`s among the hits):

- `STATE_IA_TIII_C100B_S100B.22` — 1 block(s), 400 repeated characters
- `STATE_IA_TIII_C100C_S100C.1` — 1 block(s), 400 repeated characters
- `STATE_IA_TIII_C100D_S100D.1` — 1 block(s), 400 repeated characters
- `STATE_IA_TIII_C101A_S101A.1` — 1 block(s), 400 repeated characters
- `STATE_IA_TIII_C101B_S101B.4` — 1 block(s), 399 repeated characters
- `STATE_IA_TIII_C101B_S101B.8` — 1 block(s), 400 repeated characters
- `STATE_IA_TIII_C101C_S101C.3` — 2 block(s), 800 repeated characters
- `STATE_IA_TIII_C101_S101.24` — 1 block(s), 400 repeated characters

Examples — us_id_constitutions (smallest `act_id`s among the hits):

- `SCONST_ID_AVIII_S3` — 1 block(s), 400 repeated characters
- `SCONST_ID_AVIII_S3C` — 1 block(s), 400 repeated characters

Examples — us_id_court_rules (smallest `act_id`s among the hits):

- `SRULES_ID_IAR_R10` — 1 block(s), 400 repeated characters
- `SRULES_ID_IAR_R108` — 1 block(s), 400 repeated characters
- `SRULES_ID_IAR_R11` — 3 block(s), 1,200 repeated characters
- `SRULES_ID_IAR_R118` — 1 block(s), 400 repeated characters
- `SRULES_ID_IAR_R12` — 2 block(s), 800 repeated characters
- `SRULES_ID_IAR_R12_1` — 2 block(s), 799 repeated characters
- `SRULES_ID_IAR_R12_2` — 3 block(s), 1,199 repeated characters
- `SRULES_ID_IAR_R12_3` — 2 block(s), 800 repeated characters

Examples — us_id_guidance (smallest `act_id`s among the hits):

- `ID_INS_B_16-06` — 1 block(s), 399 repeated characters
- `ID_INS_B_17-01` — 1 block(s), 400 repeated characters
- `ID_INS_B_18-01` — 4 block(s), 1,598 repeated characters
- `ID_INS_B_18-02` — 2 block(s), 798 repeated characters
- `ID_INS_B_18-03` — 1 block(s), 400 repeated characters
- `ID_INS_B_18-06` — 3 block(s), 1,199 repeated characters
- `ID_INS_B_19-02` — 1 block(s), 400 repeated characters
- `ID_INS_B_19-04` — 7 block(s), 2,798 repeated characters

Examples — us_id_regulations (smallest `act_id`s among the hits):

- `STATE_ID_IDAPA_02_01_04_010` — 2 block(s), 800 repeated characters
- `STATE_ID_IDAPA_02_01_04_200` — 1 block(s), 400 repeated characters
- `STATE_ID_IDAPA_02_01_07_010` — 1 block(s), 400 repeated characters
- `STATE_ID_IDAPA_02_01_07_300` — 2 block(s), 799 repeated characters
- `STATE_ID_IDAPA_02_01_07_500` — 1 block(s), 400 repeated characters
- `STATE_ID_IDAPA_02_01_07_700` — 1 block(s), 400 repeated characters
- `STATE_ID_IDAPA_02_01_08_101` — 1 block(s), 400 repeated characters
- `STATE_ID_IDAPA_02_02_02_120` — 2 block(s), 800 repeated characters

Examples — us_id_statutes (smallest `act_id`s among the hits):

- `STATE_ID_T11_C2_S11-203` — 1 block(s), 399 repeated characters
- `STATE_ID_T11_C4_S11-403` — 1 block(s), 400 repeated characters
- `STATE_ID_T11_C6_S11-604A` — 1 block(s), 399 repeated characters
- `STATE_ID_T11_C6_S11-605` — 1 block(s), 400 repeated characters
- `STATE_ID_T11_C7_S11-703` — 1 block(s), 399 repeated characters
- `STATE_ID_T12_C1_S12-117` — 1 block(s), 400 repeated characters
- `STATE_ID_T12_C1_S12-120` — 1 block(s), 400 repeated characters
- `STATE_ID_T14_C5_S14-5-102` — 3 block(s), 1,200 repeated characters

Examples — us_il_constitutions (smallest `act_id`s among the hits):

- `SCONST_IL_AIII_S7` — 2 block(s), 799 repeated characters
- `SCONST_IL_AIV_S2` — 1 block(s), 399 repeated characters
- `SCONST_IL_AIV_S3` — 1 block(s), 400 repeated characters
- `SCONST_IL_AIX_S11` — 2 block(s), 800 repeated characters
- `SCONST_IL_AI_S8.1` — 1 block(s), 400 repeated characters
- `SCONST_IL_AVII_S6` — 1 block(s), 399 repeated characters
- `SCONST_IL_AVI_S12` — 1 block(s), 400 repeated characters
- `SCONST_IL_AVI_S15` — 3 block(s), 1,198 repeated characters

Examples — us_il_court_rules (smallest `act_id`s among the hits):

- `SRULES_IL_TIII_R302` — 1 block(s), 400 repeated characters
- `SRULES_IL_TIII_R303` — 5 block(s), 1,998 repeated characters
- `SRULES_IL_TIII_R304` — 6 block(s), 2,397 repeated characters
- `SRULES_IL_TIII_R305` — 9 block(s), 3,600 repeated characters
- `SRULES_IL_TIII_R306` — 13 block(s), 5,198 repeated characters
- `SRULES_IL_TIII_R307` — 6 block(s), 2,400 repeated characters
- `SRULES_IL_TIII_R308` — 4 block(s), 1,600 repeated characters
- `SRULES_IL_TIII_R310_1` — 6 block(s), 2,399 repeated characters

Examples — us_il_guidance (smallest `act_id`s among the hits):

- `IL_INS_CB_2011-05` — 7 block(s), 2,798 repeated characters
- `IL_INS_CB_2011-07` — 2 block(s), 800 repeated characters
- `IL_INS_CB_2011-14` — 1 block(s), 400 repeated characters
- `IL_INS_CB_2012-08` — 2 block(s), 799 repeated characters
- `IL_INS_CB_2012-11` — 6 block(s), 2,398 repeated characters
- `IL_INS_CB_2013-04` — 1 block(s), 400 repeated characters
- `IL_INS_CB_2013-09` — 2 block(s), 800 repeated characters
- `IL_INS_CB_2014-10` — 4 block(s), 1,600 repeated characters

Examples — us_il_regulations (smallest `act_id`s among the hits):

- `STATE_IL_IAC_T11_P100_S100_10` — 3 block(s), 1,199 repeated characters
- `STATE_IL_IAC_T11_P100_S100_120` — 1 block(s), 400 repeated characters
- `STATE_IL_IAC_T11_P100_S100_130` — 1 block(s), 400 repeated characters
- `STATE_IL_IAC_T11_P100_S100_150` — 3 block(s), 1,200 repeated characters
- `STATE_IL_IAC_T11_P100_S100_160` — 1 block(s), 400 repeated characters
- `STATE_IL_IAC_T11_P100_S100_245` — 4 block(s), 1,599 repeated characters
- `STATE_IL_IAC_T11_P100_S100_250` — 2 block(s), 799 repeated characters
- `STATE_IL_IAC_T11_P100_S100_260` — 2 block(s), 799 repeated characters

Examples — us_il_statutes (smallest `act_id`s among the hits):

- `STATE_IL_C105_A105_S6c` — 1 block(s), 400 repeated characters
- `STATE_IL_C105_A125_S2.3` — 2 block(s), 799 repeated characters
- `STATE_IL_C105_A126_S15` — 1 block(s), 400 repeated characters
- `STATE_IL_C105_A126_S16` — 1 block(s), 400 repeated characters
- `STATE_IL_C105_A126_S20` — 1 block(s), 400 repeated characters
- `STATE_IL_C105_A128_S5` — 1 block(s), 400 repeated characters
- `STATE_IL_C105_A135_S5` — 1 block(s), 400 repeated characters
- `STATE_IL_C105_A13_S20` — 1 block(s), 400 repeated characters

Examples — us_in_constitutions (smallest `act_id`s among the hits):

- `SCONST_IN_A10_S1` — 2 block(s), 800 repeated characters
- `SCONST_IN_A5_S10` — 2 block(s), 800 repeated characters
- `SCONST_IN_A5_S14` — 1 block(s), 400 repeated characters
- `SCONST_IN_A7_S11` — 2 block(s), 800 repeated characters

Examples — us_in_court_rules (smallest `act_id`s among the hits):

- `SRULES_IN_ADMDISC_R12` — 9 block(s), 3,594 repeated characters
- `SRULES_IN_ADMDISC_R13_1` — 3 block(s), 1,200 repeated characters
- `SRULES_IN_ADMDISC_R13_V03011997` — 2 block(s), 800 repeated characters
- `SRULES_IN_ADMDISC_R13_V05152025` — 2 block(s), 800 repeated characters
- `SRULES_IN_ADMDISC_R15` — 2 block(s), 799 repeated characters
- `SRULES_IN_ADMDISC_R17` — 1 block(s), 400 repeated characters
- `SRULES_IN_ADMDISC_R17_1` — 1 block(s), 399 repeated characters
- `SRULES_IN_ADMDISC_R17_1_V02242021` — 1 block(s), 400 repeated characters

Examples — us_in_guidance (smallest `act_id`s among the hits):

- `IN_INS_B_1` — 1 block(s), 399 repeated characters
- `IN_INS_B_102` — 1 block(s), 399 repeated characters
- `IN_INS_B_103` — 1 block(s), 400 repeated characters
- `IN_INS_B_105` — 8 block(s), 3,195 repeated characters
- `IN_INS_B_107` — 5 block(s), 1,999 repeated characters
- `IN_INS_B_108` — 1 block(s), 400 repeated characters
- `IN_INS_B_110` — 1 block(s), 400 repeated characters
- `IN_INS_B_111` — 2 block(s), 799 repeated characters

Examples — us_in_statutes (smallest `act_id`s among the hits):

- `STATE_IN_T10_A12_C2_S10-12-2-2` — 1 block(s), 400 repeated characters
- `STATE_IN_T10_A13_C3_S10-13-3-27` — 1 block(s), 400 repeated characters
- `STATE_IN_T10_A13_C3_S10-13-3-27.5` — 1 block(s), 400 repeated characters
- `STATE_IN_T10_A13_C3_S10-13-3-36` — 1 block(s), 400 repeated characters
- `STATE_IN_T10_A13_C3_S10-13-3-38.5` — 1 block(s), 400 repeated characters
- `STATE_IN_T10_A13_C3_S10-13-3-39` — 1 block(s), 399 repeated characters
- `STATE_IN_T10_A14_C3_S10-14-3-10.8` — 2 block(s), 799 repeated characters
- `STATE_IN_T10_A14_C3_S10-14-3-12` — 1 block(s), 399 repeated characters

Examples — us_ks_constitutions (smallest `act_id`s among the hits):

- `SCONST_KS_A10_S0` — 1 block(s), 399 repeated characters
- `SCONST_KS_A11_S0` — 7 block(s), 2,798 repeated characters
- `SCONST_KS_A12_S0` — 3 block(s), 1,199 repeated characters
- `SCONST_KS_A14_S0` — 2 block(s), 800 repeated characters
- `SCONST_KS_A15_S0` — 14 block(s), 5,594 repeated characters
- `SCONST_KS_A1_S0` — 4 block(s), 1,600 repeated characters
- `SCONST_KS_A2_S0` — 6 block(s), 2,399 repeated characters
- `SCONST_KS_A3_S0` — 6 block(s), 2,397 repeated characters

Examples — us_ks_court_rules (smallest `act_id`s among the hits):

- `SRULES_KS_KSSCTR_240_RPreamble_A_Lawyer_s_Responsibilities` — 4 block(s), 1,600 repeated characters
- `SRULES_KS_KSSCTR_240_RScope_1` — 3 block(s), 1,200 repeated characters
- `SRULES_KS_KSSCTR_601B_RApplication` — 3 block(s), 1,199 repeated characters
- `SRULES_KS_KSSCTR_601B_RScope` — 1 block(s), 400 repeated characters
- `SRULES_KS_KSSCTR_601B_RTerminology` — 3 block(s), 1,198 repeated characters
- `SRULES_KS_KSSCTR_R1001` — 4 block(s), 1,600 repeated characters
- `SRULES_KS_KSSCTR_R1002` — 1 block(s), 400 repeated characters
- `SRULES_KS_KSSCTR_R103` — 2 block(s), 800 repeated characters

Examples — us_ks_guidance (smallest `act_id`s among the hits):

- `KS_INS_B_1987_06` — 3 block(s), 1,197 repeated characters
- `KS_INS_B_1987_08` — 1 block(s), 400 repeated characters
- `KS_INS_B_1987_10` — 3 block(s), 1,199 repeated characters
- `KS_INS_B_1991_04` — 1 block(s), 400 repeated characters
- `KS_INS_B_1993_21` — 1 block(s), 400 repeated characters
- `KS_INS_B_1995_19` — 1 block(s), 400 repeated characters
- `KS_INS_B_1995_21` — 2 block(s), 800 repeated characters
- `KS_INS_B_1995_22` — 2 block(s), 799 repeated characters

Examples — us_ks_statutes (smallest `act_id`s among the hits):

- `STATE_KS_C10_A1_S10-106` — 1 block(s), 400 repeated characters
- `STATE_KS_C12_A12_S12-1236` — 1 block(s), 400 repeated characters
- `STATE_KS_C12_A12_S12-1276` — 1 block(s), 400 repeated characters
- `STATE_KS_C12_A12_S12-1288` — 1 block(s), 399 repeated characters
- `STATE_KS_C12_A14_S12-1440` — 1 block(s), 400 repeated characters
- `STATE_KS_C12_A15_S12-1509` — 1 block(s), 400 repeated characters
- `STATE_KS_C12_A15_S12-1526` — 1 block(s), 400 repeated characters
- `STATE_KS_C12_A15_S12-1542` — 1 block(s), 400 repeated characters

Examples — us_ky_constitutions (smallest `act_id`s among the hits):

- `SCONST_KY_AI_S110` — 1 block(s), 399 repeated characters
- `SCONST_KY_AI_S112` — 2 block(s), 798 repeated characters
- `SCONST_KY_AI_S113` — 1 block(s), 399 repeated characters
- `SCONST_KY_AI_S118` — 1 block(s), 400 repeated characters
- `SCONST_KY_AI_S150` — 1 block(s), 400 repeated characters
- `SCONST_KY_AI_S160` — 1 block(s), 400 repeated characters
- `SCONST_KY_AI_S170` — 1 block(s), 399 repeated characters
- `SCONST_KY_AI_S171` — 1 block(s), 399 repeated characters

Examples — us_ky_guidance (smallest `act_id`s among the hits):

- `KY_INS_AO_1998-01` — 1 block(s), 400 repeated characters
- `KY_INS_AO_1998-02` — 1 block(s), 399 repeated characters
- `KY_INS_AO_1998-05` — 1 block(s), 399 repeated characters
- `KY_INS_AO_1999-01` — 1 block(s), 400 repeated characters
- `KY_INS_AO_1999-02` — 1 block(s), 400 repeated characters
- `KY_INS_AO_1999-03` — 1 block(s), 400 repeated characters
- `KY_INS_AO_1999-06` — 3 block(s), 1,199 repeated characters
- `KY_INS_AO_1999-08` — 2 block(s), 798 repeated characters

Examples — us_ky_regulations (smallest `act_id`s among the hits):

- `STATE_KY_KAR_T001_C002_R010` — 3 block(s), 1,199 repeated characters
- `STATE_KY_KAR_T001_C004_R005` — 7 block(s), 2,797 repeated characters
- `STATE_KY_KAR_T001_C005_R010` — 5 block(s), 1,998 repeated characters
- `STATE_KY_KAR_T001_C006_R020` — 1 block(s), 400 repeated characters
- `STATE_KY_KAR_T002_C002_R010` — 1 block(s), 400 repeated characters
- `STATE_KY_KAR_T002_C002_R040` — 1 block(s), 400 repeated characters
- `STATE_KY_KAR_T002_C002_R050` — 2 block(s), 799 repeated characters
- `STATE_KY_KAR_T002_C002_R060` — 2 block(s), 800 repeated characters

Examples — us_ky_statutes (smallest `act_id`s among the hits):

- `STATE_KY_TIII_C11A_S11A.010` — 1 block(s), 399 repeated characters
- `STATE_KY_TIII_C11A_S11A.040` — 2 block(s), 800 repeated characters
- `STATE_KY_TIII_C11A_S11A.047` — 1 block(s), 400 repeated characters
- `STATE_KY_TIII_C11A_S11A.050` — 1 block(s), 399 repeated characters
- `STATE_KY_TIII_C11A_S11A.080` — 1 block(s), 399 repeated characters
- `STATE_KY_TIII_C11A_S11A.201` — 2 block(s), 800 repeated characters
- `STATE_KY_TIII_C11A_S11A.211` — 2 block(s), 800 repeated characters
- `STATE_KY_TIII_C11_S11.026` — 1 block(s), 400 repeated characters

Examples — us_la_constitutions (smallest `act_id`s among the hits):

- `SCONST_LA_AIII_S18` — 1 block(s), 400 repeated characters
- `SCONST_LA_AIII_S2` — 4 block(s), 1,599 repeated characters
- `SCONST_LA_AIII_S4` — 1 block(s), 400 repeated characters
- `SCONST_LA_AIV_S18` — 1 block(s), 400 repeated characters
- `SCONST_LA_AIV_S21` — 3 block(s), 1,200 repeated characters
- `SCONST_LA_AIV_S5` — 2 block(s), 800 repeated characters
- `SCONST_LA_AI_S17` — 1 block(s), 400 repeated characters
- `SCONST_LA_AI_S4` — 4 block(s), 1,599 repeated characters

Examples — us_la_court_rules (smallest `act_id`s among the hits):

- `SRULES_LA_CJC_R3` — 11 block(s), 4,400 repeated characters
- `SRULES_LA_CJC_R4` — 1 block(s), 400 repeated characters
- `SRULES_LA_CJC_R5` — 2 block(s), 798 repeated characters
- `SRULES_LA_CJC_R6` — 6 block(s), 2,398 repeated characters
- `SRULES_LA_CJC_R7` — 13 block(s), 5,198 repeated characters
- `SRULES_LA_DCR_TII_R10_1` — 1 block(s), 399 repeated characters
- `SRULES_LA_DCR_TII_R12_1` — 1 block(s), 399 repeated characters
- `SRULES_LA_DCR_TII_R9_12` — 1 block(s), 399 repeated characters

Examples — us_la_statutes (smallest `act_id`s among the hits):

- `STATE_LA_Cchildrens-code_A1003` — 1 block(s), 399 repeated characters
- `STATE_LA_Cchildrens-code_A1015` — 1 block(s), 400 repeated characters
- `STATE_LA_Cchildrens-code_A1036.2` — 1 block(s), 400 repeated characters
- `STATE_LA_Cchildrens-code_A1107.5` — 2 block(s), 799 repeated characters
- `STATE_LA_Cchildrens-code_A1107.8` — 1 block(s), 400 repeated characters
- `STATE_LA_Cchildrens-code_A1122` — 6 block(s), 2,400 repeated characters
- `STATE_LA_Cchildrens-code_A1125` — 1 block(s), 400 repeated characters
- `STATE_LA_Cchildrens-code_A1152` — 1 block(s), 400 repeated characters

Examples — us_ma_constitutions (smallest `act_id`s among the hits):

- `SCONST_MA_A1_SIII` — 1 block(s), 399 repeated characters
- `SCONST_MA_A2.I.II_SII` — 1 block(s), 399 repeated characters
- `SCONST_MA_A2.I.I_SIV` — 2 block(s), 798 repeated characters
- `SCONST_MA_A2.II.I_SVII` — 1 block(s), 400 repeated characters
- `SCONST_MA_A2.II.I_SX` — 1 block(s), 400 repeated characters
- `SCONST_MA_A2.VI_SI` — 2 block(s), 800 repeated characters
- `SCONST_MA_A2.VI_SII` — 1 block(s), 400 repeated characters
- `SCONST_MA_AI_S2` — 72 block(s), 28,785 repeated characters

Examples — us_ma_court_rules (smallest `act_id`s among the hits):

- `SRULES_MA_MACR_R13_0` — 6 block(s), 2,400 repeated characters
- `SRULES_MA_MACR_R15_0` — 1 block(s), 399 repeated characters
- `SRULES_MA_MACR_R19_0` — 3 block(s), 1,199 repeated characters
- `SRULES_MA_MACR_R20_0` — 3 block(s), 1,200 repeated characters
- `SRULES_MA_MACR_R31_0` — 1 block(s), 400 repeated characters
- `SRULES_MA_MACR_R6_0` — 5 block(s), 2,000 repeated characters
- `SRULES_MA_MBAIL_R43` — 1 block(s), 400 repeated characters
- `SRULES_MA_MBMCSO_R1_23` — 3 block(s), 1,200 repeated characters

Examples — us_ma_guidance (smallest `act_id`s among the hits):

- `MA_INS_1997_01_COVERAGE_FOR_MINIMUM_HOSPITAL_STAYS_AND_POSTPARTUM_CARE` — 3 block(s), 1,200 repeated characters
- `MA_INS_1997_02_CLAIM_REPAIR_PRACTICES` — 1 block(s), 400 repeated characters
- `MA_INS_1997_03_ATTACHMENT_TO_1997_GUIDE_TO_HEALTH_INSURANCE_FOR_PEOPLE_WITH_MEDICARE` — 18 block(s), 7,197 repeated characters
- `MA_INS_1997_04_MANDATED_OUTPATIENT_MENTAL_HEALTH_AND_ALCOHOLISM_TREATMENT_BENEFITS` — 1 block(s), 400 repeated characters
- `MA_INS_1997_05_THE_SMALL_GROUP_CONTINUATION_OF_COVERAGE_LAW` — 1 block(s), 399 repeated characters
- `MA_INS_1997_06_BUSINESS_LICENSE_TAX_INVOICES_FROM_THE_TOWN_OF_QUINWOOD_WEST_VIRGINIA` — 2 block(s), 800 repeated characters
- `MA_INS_1997_07_IMPLEMENTATION_OF_THE_MASSACHUSETTS_NONGROUP_HEALTH_INSURANCE_LAW_0` — 46 block(s), 18,394 repeated characters
- `MA_INS_1997_08_REQUIRED_OPEN_ENROLLMENT_PERIOD_TO_BE_HELD_SEPTEMBER_15_1997_THROUGH_NOVEMBER_14_1997_PURSUANT_TO_MGL_C_176K` — 1 block(s), 400 repeated characters

Examples — us_ma_statutes (smallest `act_id`s among the hits):

- `STATE_MA_PIII_TIII_C239_S15` — 1 block(s), 400 repeated characters
- `STATE_MA_PIII_TIII_C239_S16` — 8 block(s), 3,199 repeated characters
- `STATE_MA_PIII_TIII_C239_S2A` — 1 block(s), 400 repeated characters
- `STATE_MA_PIII_TIII_C239_S3` — 2 block(s), 799 repeated characters
- `STATE_MA_PIII_TIII_C239_S4` — 5 block(s), 1,999 repeated characters
- `STATE_MA_PIII_TIII_C239_S5` — 4 block(s), 1,600 repeated characters
- `STATE_MA_PIII_TIII_C239_S8A` — 4 block(s), 1,598 repeated characters
- `STATE_MA_PIII_TIII_C239_S9` — 1 block(s), 400 repeated characters

Examples — us_md_constitutions (smallest `act_id`s among the hits):

- `SCONST_MD_A1_S0` — 11 block(s), 4,400 repeated characters
- `SCONST_MD_A1_S1` — 15 block(s), 5,996 repeated characters
- `SCONST_MD_AIII_S13` — 2 block(s), 798 repeated characters
- `SCONST_MD_AIII_S15` — 1 block(s), 400 repeated characters
- `SCONST_MD_AIII_S34` — 1 block(s), 400 repeated characters
- `SCONST_MD_AIII_S40A` — 1 block(s), 400 repeated characters
- `SCONST_MD_AIII_S52` — 7 block(s), 2,799 repeated characters
- `SCONST_MD_AIII_S61` — 2 block(s), 800 repeated characters

Examples — us_md_court_rules (smallest `act_id`s among the hits):

- `SRULES_MD_T10_R10_103` — 3 block(s), 1,200 repeated characters
- `SRULES_MD_T10_R10_106` — 5 block(s), 1,998 repeated characters
- `SRULES_MD_T10_R10_106_1` — 1 block(s), 400 repeated characters
- `SRULES_MD_T10_R10_108` — 2 block(s), 799 repeated characters
- `SRULES_MD_T10_R10_111` — 4 block(s), 1,600 repeated characters
- `SRULES_MD_T10_R10_112` — 5 block(s), 1,999 repeated characters
- `SRULES_MD_T10_R10_201` — 4 block(s), 1,600 repeated characters
- `SRULES_MD_T10_R10_202` — 2 block(s), 799 repeated characters

Examples — us_md_guidance (smallest `act_id`s among the hits):

- `MD_INS_B_00-02` — 1 block(s), 400 repeated characters
- `MD_INS_B_00-05` — 1 block(s), 400 repeated characters
- `MD_INS_B_00-06` — 2 block(s), 800 repeated characters
- `MD_INS_B_00-07` — 2 block(s), 800 repeated characters
- `MD_INS_B_00-08` — 2 block(s), 799 repeated characters
- `MD_INS_B_00-09` — 1 block(s), 400 repeated characters
- `MD_INS_B_00-11` — 3 block(s), 1,199 repeated characters
- `MD_INS_B_00-12` — 1 block(s), 400 repeated characters

Examples — us_md_regulations (smallest `act_id`s among the hits):

- `STATE_MD_COMAR_02_02_01_05` — 1 block(s), 400 repeated characters
- `STATE_MD_COMAR_02_02_01_09` — 2 block(s), 800 repeated characters
- `STATE_MD_COMAR_02_02_02_01` — 1 block(s), 400 repeated characters
- `STATE_MD_COMAR_02_02_03_01` — 24 block(s), 9,596 repeated characters
- `STATE_MD_COMAR_02_02_03_07` — 1 block(s), 400 repeated characters
- `STATE_MD_COMAR_02_02_03_08` — 2 block(s), 800 repeated characters
- `STATE_MD_COMAR_02_02_03_10` — 1 block(s), 400 repeated characters
- `STATE_MD_COMAR_02_02_03_12` — 4 block(s), 1,600 repeated characters

Examples — us_md_statutes (smallest `act_id`s among the hits):

- `STATE_MD_Agab_T11_S11_S11-1102` — 1 block(s), 400 repeated characters
- `STATE_MD_Agab_T11_S16_S11-1607` — 1 block(s), 400 repeated characters
- `STATE_MD_Agab_T12_S10_S12-1002.1` — 1 block(s), 400 repeated characters
- `STATE_MD_Agab_T12_S16_S12-1603` — 3 block(s), 1,198 repeated characters
- `STATE_MD_Agab_T12_S16_S12-1604` — 2 block(s), 799 repeated characters
- `STATE_MD_Agab_T12_S16_S12-1605` — 2 block(s), 800 repeated characters
- `STATE_MD_Agab_T12_S20_S12-2004` — 2 block(s), 800 repeated characters
- `STATE_MD_Agab_T12_S20_S12-2005` — 2 block(s), 800 repeated characters

Examples — us_me_constitutions (smallest `act_id`s among the hits):

- `SCONST_ME_AIV-2_S2` — 1 block(s), 399 repeated characters
- `SCONST_ME_AIV-3_S1-A` — 1 block(s), 400 repeated characters
- `SCONST_ME_AIV-3_S17` — 1 block(s), 400 repeated characters
- `SCONST_ME_AIV-3_S18` — 1 block(s), 399 repeated characters
- `SCONST_ME_AIV-3_S20` — 2 block(s), 799 repeated characters
- `SCONST_ME_AIX_S14` — 1 block(s), 400 repeated characters
- `SCONST_ME_AIX_S24` — 1 block(s), 400 repeated characters
- `SCONST_ME_AIX_S25` — 1 block(s), 400 repeated characters

Examples — us_me_court_rules (smallest `act_id`s among the hits):

- `SRULES_ME_APP_R10` — 1 block(s), 399 repeated characters
- `SRULES_ME_APP_R11` — 1 block(s), 399 repeated characters
- `SRULES_ME_APP_R12A` — 1 block(s), 399 repeated characters
- `SRULES_ME_APP_R12B` — 1 block(s), 399 repeated characters
- `SRULES_ME_APP_R13` — 1 block(s), 399 repeated characters
- `SRULES_ME_APP_R14` — 3 block(s), 1,196 repeated characters
- `SRULES_ME_APP_R19` — 6 block(s), 2,394 repeated characters
- `SRULES_ME_APP_R1A` — 1 block(s), 400 repeated characters

Examples — us_me_guidance (smallest `act_id`s among the hits):

- `ME_INS_B_146` — 1 block(s), 400 repeated characters
- `ME_INS_B_159` — 2 block(s), 800 repeated characters
- `ME_INS_B_161` — 1 block(s), 399 repeated characters
- `ME_INS_B_164` — 1 block(s), 400 repeated characters
- `ME_INS_B_166` — 1 block(s), 400 repeated characters
- `ME_INS_B_168` — 3 block(s), 1,200 repeated characters
- `ME_INS_B_176` — 10 block(s), 3,997 repeated characters
- `ME_INS_B_194` — 1 block(s), 400 repeated characters

Examples — us_me_regulations (smallest `act_id`s among the hits):

- `STATE_ME_CMR_00_000_1` — 5 block(s), 1,999 repeated characters
- `STATE_ME_CMR_00_001_1` — 27 block(s), 10,791 repeated characters
- `STATE_ME_CMR_00_002_1` — 71 block(s), 28,391 repeated characters
- `STATE_ME_CMR_00_002_2` — 7 block(s), 2,800 repeated characters
- `STATE_ME_CMR_00_002_3` — 8 block(s), 3,199 repeated characters
- `STATE_ME_CMR_00_002_4` — 15 block(s), 5,998 repeated characters
- `STATE_ME_CMR_00_002_5` — 9 block(s), 3,599 repeated characters
- `STATE_ME_CMR_00_002_6` — 6 block(s), 2,400 repeated characters

Examples — us_me_statutes (smallest `act_id`s among the hits):

- `STATE_ME_T10_P11_C951_S9002` — 1 block(s), 400 repeated characters
- `STATE_ME_T10_P11_C951_S9021` — 1 block(s), 400 repeated characters
- `STATE_ME_T10_P11_C951_S9042` — 1 block(s), 400 repeated characters
- `STATE_ME_T10_P11_C953_S9094` — 1 block(s), 400 repeated characters
- `STATE_ME_T10_P11_C953_S9094-A` — 3 block(s), 1,199 repeated characters
- `STATE_ME_T10_P11_C953_S9097` — 5 block(s), 2,000 repeated characters
- `STATE_ME_T10_P11_C953_S9098` — 1 block(s), 400 repeated characters
- `STATE_ME_T10_P11_C953_S9099` — 1 block(s), 400 repeated characters

Examples — us_mi_constitutions (smallest `act_id`s among the hits):

- `SCONST_MI_AII_S9` — 2 block(s), 800 repeated characters
- `SCONST_MI_AIV_S12` — 1 block(s), 400 repeated characters
- `SCONST_MI_AIV_S2` — 1 block(s), 400 repeated characters
- `SCONST_MI_AIV_S3` — 1 block(s), 400 repeated characters
- `SCONST_MI_AIV_S6` — 2 block(s), 800 repeated characters
- `SCONST_MI_AIX_S16` — 1 block(s), 400 repeated characters
- `SCONST_MI_AIX_S26` — 1 block(s), 400 repeated characters
- `SCONST_MI_AIX_S35` — 2 block(s), 800 repeated characters

Examples — us_mi_court_rules (smallest `act_id`s among the hits):

- `SRULES_MI_AO_R1981_7` — 43 block(s), 17,177 repeated characters
- `SRULES_MI_AO_R1985_5` — 12 block(s), 4,794 repeated characters
- `SRULES_MI_AO_R1989_1` — 4 block(s), 1,595 repeated characters
- `SRULES_MI_AO_R1989_3` — 8 block(s), 3,194 repeated characters
- `SRULES_MI_AO_R1990_2` — 2 block(s), 798 repeated characters
- `SRULES_MI_AO_R1990_3` — 1 block(s), 399 repeated characters
- `SRULES_MI_AO_R1990_8` — 1 block(s), 400 repeated characters
- `SRULES_MI_AO_R1991_7` — 1 block(s), 400 repeated characters

Examples — us_mi_guidance (smallest `act_id`s among the hits):

- `MI_INS_2006_04_INS` — 3 block(s), 1,199 repeated characters
- `MI_INS_2006_05_INS` — 1 block(s), 398 repeated characters
- `MI_INS_2006_08_INS` — 3 block(s), 1,198 repeated characters
- `MI_INS_2006_09_INS` — 2 block(s), 800 repeated characters
- `MI_INS_2007_07_INS` — 2 block(s), 800 repeated characters
- `MI_INS_2007_09_INS` — 1 block(s), 399 repeated characters
- `MI_INS_2008_01_INS` — 3 block(s), 1,200 repeated characters
- `MI_INS_2008_05_INS` — 2 block(s), 800 repeated characters

Examples — us_mi_statutes (smallest `act_id`s among the hits):

- `STATE_MI_C10_AE-R-O-No-1995-5_S10.151` — 2 block(s), 800 repeated characters
- `STATE_MI_C10_AE-R-O-No-2000-1_S10.152` — 1 block(s), 400 repeated characters
- `STATE_MI_C10_AE-R-O-No-2002-7_S10.153` — 1 block(s), 400 repeated characters
- `STATE_MI_C117_AAct-279-of-1909_S117.14` — 2 block(s), 800 repeated characters
- `STATE_MI_C117_AAct-279-of-1909_S117.14a` — 1 block(s), 400 repeated characters
- `STATE_MI_C117_AAct-279-of-1909_S117.15` — 1 block(s), 400 repeated characters
- `STATE_MI_C117_AAct-279-of-1909_S117.18` — 1 block(s), 400 repeated characters
- `STATE_MI_C117_AAct-279-of-1909_S117.25` — 1 block(s), 400 repeated characters

Examples — us_mn_court_rules (smallest `act_id`s among the hits):

- `SRULES_MN_AP_FLAM_R13` — 1 block(s), 399 repeated characters
- `SRULES_MN_AP_RCAP_R103` — 3 block(s), 1,199 repeated characters
- `SRULES_MN_AP_RCAP_R104` — 1 block(s), 400 repeated characters
- `SRULES_MN_AP_RCAP_R105` — 2 block(s), 798 repeated characters
- `SRULES_MN_AP_RCAP_R107` — 1 block(s), 400 repeated characters
- `SRULES_MN_AP_RCAP_R108` — 4 block(s), 1,600 repeated characters
- `SRULES_MN_AP_RCAP_R109` — 2 block(s), 799 repeated characters
- `SRULES_MN_AP_RCAP_R110_01` — 6 block(s), 2,400 repeated characters

Examples — us_mn_guidance (smallest `act_id`s among the hits):

- `MN_INS_AB_2010-4` — 4 block(s), 1,598 repeated characters
- `MN_INS_AB_2016-1` — 6 block(s), 2,396 repeated characters
- `MN_INS_AB_2016-2` — 2 block(s), 800 repeated characters
- `MN_INS_AB_2017-1` — 11 block(s), 4,395 repeated characters
- `MN_INS_AB_2018-1` — 10 block(s), 3,991 repeated characters
- `MN_INS_AB_2019-1` — 11 block(s), 4,390 repeated characters
- `MN_INS_AB_2019-2` — 3 block(s), 1,200 repeated characters
- `MN_INS_AB_2019-5` — 1 block(s), 400 repeated characters

Examples — us_mn_regulations (smallest `act_id`s among the hits):

- `STATE_MN_ADR_1105_0100` — 3 block(s), 1,198 repeated characters
- `STATE_MN_ADR_1105_0250` — 1 block(s), 400 repeated characters
- `STATE_MN_ADR_1105_1400` — 2 block(s), 799 repeated characters
- `STATE_MN_ADR_1105_1500` — 1 block(s), 400 repeated characters
- `STATE_MN_ADR_1105_2200` — 2 block(s), 800 repeated characters
- `STATE_MN_ADR_1105_2500` — 3 block(s), 1,200 repeated characters
- `STATE_MN_ADR_1105_2540` — 1 block(s), 400 repeated characters
- `STATE_MN_ADR_1105_3000` — 3 block(s), 1,199 repeated characters

Examples — us_mn_statutes (smallest `act_id`s among the hits):

- `STATE_MN_P103A_114B_C103B_S103B.101` — 4 block(s), 1,600 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.211` — 1 block(s), 400 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.231` — 4 block(s), 1,600 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.235` — 1 block(s), 400 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.245` — 1 block(s), 400 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.251` — 1 block(s), 400 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.255` — 2 block(s), 799 repeated characters
- `STATE_MN_P103A_114B_C103B_S103B.314` — 1 block(s), 399 repeated characters

Examples — us_mo_constitutions (smallest `act_id`s among the hits):

- `SCONST_MO_AIII_S2` — 1 block(s), 400 repeated characters
- `SCONST_MO_AIII_S3` — 7 block(s), 2,798 repeated characters
- `SCONST_MO_AIII_S37(a)` — 4 block(s), 1,599 repeated characters
- `SCONST_MO_AIII_S37(b)` — 3 block(s), 1,199 repeated characters
- `SCONST_MO_AIII_S37(c)` — 3 block(s), 1,199 repeated characters
- `SCONST_MO_AIII_S37(d)` — 5 block(s), 1,998 repeated characters
- `SCONST_MO_AIII_S37(e)` — 4 block(s), 1,600 repeated characters
- `SCONST_MO_AIII_S37(f)` — 4 block(s), 1,600 repeated characters

Examples — us_mo_guidance (smallest `act_id`s among the hits):

- `MO_INS_B_2007_01` — 3 block(s), 1,199 repeated characters
- `MO_INS_B_2011_01` — 2 block(s), 799 repeated characters
- `MO_INS_B_2012_01` — 2 block(s), 800 repeated characters
- `MO_INS_B_2013_06` — 1 block(s), 400 repeated characters
- `MO_INS_B_2015_02` — 2 block(s), 800 repeated characters
- `MO_INS_B_2015_03` — 2 block(s), 796 repeated characters
- `MO_INS_B_2016_01` — 2 block(s), 797 repeated characters
- `MO_INS_B_2016_02` — 1 block(s), 400 repeated characters

Examples — us_mo_statutes (smallest `act_id`s among the hits):

- `STATE_MO_C100_S100.050` — 1 block(s), 400 repeated characters
- `STATE_MO_C100_S100.240` — 3 block(s), 1,199 repeated characters
- `STATE_MO_C100_S100.255` — 2 block(s), 800 repeated characters
- `STATE_MO_C100_S100.270` — 2 block(s), 799 repeated characters
- `STATE_MO_C100_S100.275` — 1 block(s), 400 repeated characters
- `STATE_MO_C100_S100.286` — 2 block(s), 800 repeated characters
- `STATE_MO_C100_S100.310` — 1 block(s), 400 repeated characters
- `STATE_MO_C100_S100.390` — 1 block(s), 400 repeated characters

Examples — us_ms_constitutions (smallest `act_id`s among the hits):

- `SCONST_MS_A13_S254` — 2 block(s), 800 repeated characters
- `SCONST_MS_A15_S273` — 13 block(s), 5,197 repeated characters
- `SCONST_MS_A15_S285` — 3 block(s), 1,200 repeated characters
- `SCONST_MS_A3_S26` — 1 block(s), 400 repeated characters
- `SCONST_MS_A3_S29` — 1 block(s), 400 repeated characters
- `SCONST_MS_A4_S112` — 2 block(s), 800 repeated characters
- `SCONST_MS_A4_S90` — 1 block(s), 400 repeated characters
- `SCONST_MS_A5_S131` — 1 block(s), 399 repeated characters

Examples — us_ms_court_rules (smallest `act_id`s among the hits):

- `SRULES_MS_AEFAP_R1` — 1 block(s), 399 repeated characters
- `SRULES_MS_AEFAP_R2` — 1 block(s), 400 repeated characters
- `SRULES_MS_AEFAP_R3` — 4 block(s), 1,597 repeated characters
- `SRULES_MS_AEFAP_R4` — 1 block(s), 399 repeated characters
- `SRULES_MS_AEFAP_R6` — 2 block(s), 800 repeated characters
- `SRULES_MS_MCACE_R2` — 1 block(s), 400 repeated characters
- `SRULES_MS_MCACE_R3` — 1 block(s), 400 repeated characters
- `SRULES_MS_MCACE_R4` — 1 block(s), 400 repeated characters

Examples — us_ms_guidance (smallest `act_id`s among the hits):

- `MS_INS_B_1980-01` — 3 block(s), 1,200 repeated characters
- `MS_INS_B_1980-02A` — 1 block(s), 400 repeated characters
- `MS_INS_B_1991-04` — 1 block(s), 400 repeated characters
- `MS_INS_B_1991-2181` — 1 block(s), 400 repeated characters
- `MS_INS_B_1993-01` — 2 block(s), 799 repeated characters
- `MS_INS_B_1993-02` — 1 block(s), 400 repeated characters
- `MS_INS_B_1993-03` — 7 block(s), 2,799 repeated characters
- `MS_INS_B_1993-04` — 13 block(s), 5,198 repeated characters

Examples — us_ms_statutes (smallest `act_id`s among the hits):

- `STATE_MS_T11_C11_S27-81` — 1 block(s), 400 repeated characters
- `STATE_MS_T11_C11_S35-23` — 1 block(s), 400 repeated characters
- `STATE_MS_T11_C11_S46-1` — 1 block(s), 400 repeated characters
- `STATE_MS_T11_C11_S46-17` — 1 block(s), 400 repeated characters
- `STATE_MS_T11_C11_S46-19` — 1 block(s), 400 repeated characters
- `STATE_MS_T11_C11_S46-7` — 1 block(s), 400 repeated characters
- `STATE_MS_T11_C11_S46-9` — 1 block(s), 399 repeated characters
- `STATE_MS_T11_C11_S57-3` — 1 block(s), 400 repeated characters

Examples — us_mt_constitutions (smallest `act_id`s among the hits):

- `SCONST_MT_AI_S13` — 1 block(s), 400 repeated characters
- `SCONST_MT_AVIII_S13` — 1 block(s), 400 repeated characters

Examples — us_mt_court_rules (smallest `act_id`s among the hits):

- `SRULES_MT_MRAPP_FORM_R1` — 1 block(s), 400 repeated characters
- `SRULES_MT_MRAPP_FORM_R2` — 1 block(s), 400 repeated characters
- `SRULES_MT_MRAPP_FORM_R3` — 1 block(s), 400 repeated characters
- `SRULES_MT_MRAPP_FORM_R4` — 1 block(s), 400 repeated characters
- `SRULES_MT_MRAPP_FORM_R9` — 1 block(s), 399 repeated characters
- `SRULES_MT_MRAPP_R10` — 4 block(s), 1,599 repeated characters
- `SRULES_MT_MRAPP_R11` — 3 block(s), 1,200 repeated characters
- `SRULES_MT_MRAPP_R12` — 4 block(s), 1,599 repeated characters

Examples — us_mt_guidance (smallest `act_id`s among the hits):

- `MT_INS_AM_1995_10_10_ADVISORY_MEMO_RE_TEMPORARY_EXTENSION_OF_FORM_FILING_REQUIREMENTS` — 1 block(s), 400 repeated characters
- `MT_INS_AM_1996_06_18_ADVISORY_MEMO_RE_UNIFORM_HEALTH_BENEFIT_PLAN_FORM_FILING_REQUIREMENTS` — 2 block(s), 800 repeated characters
- `MT_INS_AM_2003_08_25_LONG_TERM_CARE_DISCOUNTS` — 1 block(s), 400 repeated characters
- `MT_INS_AM_2005_05_11_NEW_DISCOUNT_CARD_LEGISLATION_SB_380` — 1 block(s), 399 repeated characters
- `MT_INS_AM_2005_06_01_CREDIT_HISTORY_CHECKLIST_1` — 6 block(s), 2,400 repeated characters
- `MT_INS_AM_2005_06_01_NEW_CREDIT_HISTORY_AND_INSURANCE_SCORE_SB_311` — 10 block(s), 3,997 repeated characters
- `MT_INS_AM_2006_01_30_MARKETING_MEDICARE_PART_D` — 1 block(s), 400 repeated characters
- `MT_INS_AM_2006_04_14_MEDICAL_CARE_DISCOUNT_CARD_PRODUCTS` — 2 block(s), 800 repeated characters

Examples — us_mt_statutes (smallest `act_id`s among the hits):

- `STATE_MT_T10_C1_P10_S10-1-1007` — 1 block(s), 400 repeated characters
- `STATE_MT_T10_C2_P1_S10-2-102` — 1 block(s), 400 repeated characters
- `STATE_MT_T10_C2_P1_S10-2-111` — 1 block(s), 400 repeated characters
- `STATE_MT_T10_C3_P10_S10-3-1001` — 3 block(s), 1,200 repeated characters
- `STATE_MT_T10_C3_P12_S10-3-1204` — 1 block(s), 399 repeated characters
- `STATE_MT_T10_C3_P1_S10-3-102` — 1 block(s), 400 repeated characters
- `STATE_MT_T10_C3_P1_S10-3-103` — 1 block(s), 400 repeated characters
- `STATE_MT_T10_C3_P2_S10-3-207` — 1 block(s), 400 repeated characters

Examples — us_nc_constitutions (smallest `act_id`s among the hits):

- `SCONST_NC_AIII_S7` — 1 block(s), 400 repeated characters
- `SCONST_NC_AII_S22` — 1 block(s), 400 repeated characters
- `SCONST_NC_AI_S37` — 2 block(s), 800 repeated characters
- `SCONST_NC_AV_S14` — 1 block(s), 400 repeated characters
- `SCONST_NC_AV_S2` — 1 block(s), 400 repeated characters
- `SCONST_NC_AV_S4` — 1 block(s), 399 repeated characters

Examples — us_nc_court_rules (smallest `act_id`s among the hits):

- `SRULES_NC_NCARB_R2` — 3 block(s), 1,198 repeated characters
- `SRULES_NC_NCARB_R3` — 1 block(s), 397 repeated characters
- `SRULES_NC_NCARB_R4` — 1 block(s), 400 repeated characters
- `SRULES_NC_NCARB_R5` — 1 block(s), 398 repeated characters
- `SRULES_NC_NCARB_R6` — 9 block(s), 3,592 repeated characters
- `SRULES_NC_NCARB_R9` — 5 block(s), 1,996 repeated characters
- `SRULES_NC_NCBCR_Appendix_R1` — 3 block(s), 1,197 repeated characters
- `SRULES_NC_NCBCR_Appendix_R2` — 3 block(s), 1,198 repeated characters

Examples — us_nc_guidance (smallest `act_id`s among the hits):

- `NC_INS_B_15-B-01` — 11 block(s), 4,399 repeated characters
- `NC_INS_B_15-B-04` — 2 block(s), 800 repeated characters
- `NC_INS_B_15-B-05` — 12 block(s), 4,791 repeated characters
- `NC_INS_B_16-B-03` — 2 block(s), 800 repeated characters
- `NC_INS_B_16-B-05` — 1 block(s), 400 repeated characters
- `NC_INS_B_16-B-06` — 1 block(s), 400 repeated characters
- `NC_INS_B_16-B-07` — 1 block(s), 400 repeated characters
- `NC_INS_B_16-B-08` — 3 block(s), 1,200 repeated characters

Examples — us_nd_constitutions (smallest `act_id`s among the hits):

- `SCONST_ND_AIV_S13` — 1 block(s), 400 repeated characters
- `SCONST_ND_AIX_S12` — 1 block(s), 400 repeated characters
- `SCONST_ND_AIX_S6` — 2 block(s), 800 repeated characters
- `SCONST_ND_AI_S25` — 4 block(s), 1,598 repeated characters
- `SCONST_ND_AVIII_S6` — 6 block(s), 2,400 repeated characters
- `SCONST_ND_AXIV_S2` — 1 block(s), 400 repeated characters
- `SCONST_ND_AX_S12` — 1 block(s), 400 repeated characters
- `SCONST_ND_AX_S14` — 2 block(s), 799 repeated characters

Examples — us_nd_court_rules (smallest `act_id`s among the hits):

- `SRULES_ND_ADMISSIONTOPRACTICER_R1` — 1 block(s), 400 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10` — 2 block(s), 800 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10_V19990101_19990301` — 2 block(s), 800 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10_V19990301_19990809` — 2 block(s), 800 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10_V19990809_20010801` — 2 block(s), 799 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10_V20010801_20040616` — 2 block(s), 800 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10_V20040616_20090301` — 2 block(s), 800 repeated characters
- `SRULES_ND_ADMISSIONTOPRACTICER_R10_V20090301_20100901` — 2 block(s), 800 repeated characters

Examples — us_nd_guidance (smallest `act_id`s among the hits):

- `ND_INS_B_1970-004` — 1 block(s), 400 repeated characters
- `ND_INS_B_1972-012` — 41 block(s), 16,395 repeated characters
- `ND_INS_B_1974-017` — 2 block(s), 800 repeated characters
- `ND_INS_B_1975-002` — 1 block(s), 400 repeated characters
- `ND_INS_B_1975-020` — 6 block(s), 2,384 repeated characters
- `ND_INS_B_1975-021` — 1 block(s), 400 repeated characters
- `ND_INS_B_1981-001` — 5 block(s), 1,998 repeated characters
- `ND_INS_B_1981-003` — 1 block(s), 399 repeated characters

Examples — us_nd_statutes (smallest `act_id`s among the hits):

- `STATE_ND_T10_C10-01.1_S10-01.1-02` — 2 block(s), 800 repeated characters
- `STATE_ND_T10_C10-04_S10-04-02` — 4 block(s), 1,599 repeated characters
- `STATE_ND_T10_C10-04_S10-04-03` — 1 block(s), 400 repeated characters
- `STATE_ND_T10_C10-04_S10-04-05` — 2 block(s), 799 repeated characters
- `STATE_ND_T10_C10-04_S10-04-06` — 8 block(s), 3,199 repeated characters
- `STATE_ND_T10_C10-04_S10-04-07.1` — 1 block(s), 400 repeated characters
- `STATE_ND_T10_C10-04_S10-04-07.2` — 1 block(s), 400 repeated characters
- `STATE_ND_T10_C10-04_S10-04-08` — 3 block(s), 1,200 repeated characters

Examples — us_ne_constitutions (smallest `act_id`s among the hits):

- `SCONST_NE_AI-30_S0` — 1 block(s), 400 repeated characters
- `SCONST_NE_AIII-17_S0` — 1 block(s), 400 repeated characters
- `SCONST_NE_AIII-18_S0` — 1 block(s), 400 repeated characters
- `SCONST_NE_AIII-24_S0` — 2 block(s), 800 repeated characters
- `SCONST_NE_AIII-29_S0` — 1 block(s), 400 repeated characters
- `SCONST_NE_AIII_S17` — 1 block(s), 400 repeated characters
- `SCONST_NE_AIII_S18` — 1 block(s), 400 repeated characters
- `SCONST_NE_AIII_S2` — 1 block(s), 400 repeated characters

Examples — us_ne_court_rules (smallest `act_id`s among the hits):

- `SRULES_NE_NECTR_A3_Dapplication` — 1 block(s), 400 repeated characters
- `SRULES_NE_NECTR_A3_Ddefinitions` — 2 block(s), 800 repeated characters
- `SRULES_NE_NECTR_A3_Dscope` — 1 block(s), 399 repeated characters
- `SRULES_NE_NECTR_A3_Dterminology` — 4 block(s), 1,599 repeated characters
- `SRULES_NE_NECTR_A4_Dappendix` — 1 block(s), 399 repeated characters
- `SRULES_NE_NECTR_A5_Dpreamble_lawyers_responsibilities` — 4 block(s), 1,600 repeated characters
- `SRULES_NE_NECTR_A5_Dscope` — 3 block(s), 1,200 repeated characters
- `SRULES_NE_NECTR_S1_103` — 2 block(s), 800 repeated characters

Examples — us_ne_guidance (smallest `act_id`s among the hits):

- `NE_INS_CB_022` — 3 block(s), 1,199 repeated characters
- `NE_INS_CB_038` — 3 block(s), 1,199 repeated characters
- `NE_INS_CB_049` — 1 block(s), 400 repeated characters
- `NE_INS_CB_050` — 11 block(s), 4,396 repeated characters
- `NE_INS_CB_056` — 1 block(s), 400 repeated characters
- `NE_INS_CB_064` — 3 block(s), 1,200 repeated characters
- `NE_INS_CB_068` — 1 block(s), 400 repeated characters
- `NE_INS_CB_069` — 1 block(s), 400 repeated characters

Examples — us_ne_statutes (smallest `act_id`s among the hits):

- `STATE_NE_C10_S10-401` — 5 block(s), 1,999 repeated characters
- `STATE_NE_C10_S10-409` — 2 block(s), 799 repeated characters
- `STATE_NE_C10_S10-702` — 1 block(s), 399 repeated characters
- `STATE_NE_C10_S10-703.01` — 1 block(s), 399 repeated characters
- `STATE_NE_C11_S11-101` — 1 block(s), 400 repeated characters
- `STATE_NE_C11_S11-103` — 1 block(s), 400 repeated characters
- `STATE_NE_C11_S11-105` — 1 block(s), 399 repeated characters
- `STATE_NE_C11_S11-112` — 1 block(s), 400 repeated characters

Examples — us_nh_constitutions (smallest `act_id`s among the hits):

- `SCONST_NH_A1_S0` — 32 block(s), 12,793 repeated characters
- `SCONST_NH_A1_S11` — 1 block(s), 400 repeated characters
- `SCONST_NH_A2_S100` — 1 block(s), 400 repeated characters
- `SCONST_NH_A2_S49` — 1 block(s), 400 repeated characters
- `SCONST_NH_A2_S49-a` — 1 block(s), 400 repeated characters
- `SCONST_NH_A2_S5` — 1 block(s), 400 repeated characters
- `SCONST_NH_A2_S83` — 1 block(s), 400 repeated characters

Examples — us_nh_court_rules (smallest `act_id`s among the hits):

- `SRULES_NH_CIRDIST_ALTERNATIVES_TO_TRIAL_R3_30` — 8 block(s), 3,200 repeated characters
- `SRULES_NH_CIRDIST_COMMENCEMENT_OF_ACTION_R3_5` — 1 block(s), 400 repeated characters
- `SRULES_NH_CIRDIST_DISCOVERY_R3_21` — 4 block(s), 1,599 repeated characters
- `SRULES_NH_CIRDIST_DISCOVERY_R3_22` — 1 block(s), 399 repeated characters
- `SRULES_NH_CIRDIST_DISCOVERY_R3_23` — 4 block(s), 1,600 repeated characters
- `SRULES_NH_CIRDIST_DISCOVERY_R3_24` — 1 block(s), 399 repeated characters
- `SRULES_NH_CIRDIST_DISCOVERY_R3_25` — 1 block(s), 400 repeated characters
- `SRULES_NH_CIRDIST_DISCOVERY_R3_26` — 4 block(s), 1,600 repeated characters

Examples — us_nh_guidance (smallest `act_id`s among the hits):

- `NH_INS_B_2002-027-AB` — 18 block(s), 7,195 repeated characters
- `NH_INS_B_2003-051-AB` — 1 block(s), 400 repeated characters
- `NH_INS_B_2004-002-AB` — 2 block(s), 798 repeated characters
- `NH_INS_B_2005-025-AP` — 3 block(s), 1,199 repeated characters
- `NH_INS_B_2005-039-AP` — 1 block(s), 400 repeated characters
- `NH_INS_B_2005-039-AP_INS05039PLAN` — 46 block(s), 18,379 repeated characters
- `NH_INS_B_2005-044-AB` — 1 block(s), 400 repeated characters
- `NH_INS_B_2005-048-AB` — 1 block(s), 399 repeated characters

Examples — us_nh_statutes (smallest `act_id`s among the hits):

- `STATE_NH_TIII_C31_S39-d` — 1 block(s), 400 repeated characters
- `STATE_NH_TIII_C31_S5` — 1 block(s), 400 repeated characters
- `STATE_NH_TIII_C32_S5` — 2 block(s), 800 repeated characters
- `STATE_NH_TIII_C32_S5-b` — 1 block(s), 400 repeated characters
- `STATE_NH_TIII_C32_S5-f` — 1 block(s), 399 repeated characters
- `STATE_NH_TIII_C33-A_S3-a` — 3 block(s), 1,199 repeated characters
- `STATE_NH_TIII_C33_S20` — 1 block(s), 400 repeated characters
- `STATE_NH_TIII_C33_S3-g` — 1 block(s), 400 repeated characters

Examples — us_nj_constitutions (smallest `act_id`s among the hits):

- `SCONST_NJ_AII.II_S1` — 2 block(s), 800 repeated characters
- `SCONST_NJ_AII_S0` — 6 block(s), 2,399 repeated characters
- `SCONST_NJ_AIV.VII_S13` — 1 block(s), 400 repeated characters
- `SCONST_NJ_AIV.VII_S2` — 4 block(s), 1,598 repeated characters
- `SCONST_NJ_AIV_S0` — 14 block(s), 5,597 repeated characters
- `SCONST_NJ_AIX_S0` — 1 block(s), 400 repeated characters
- `SCONST_NJ_AI_S0` — 5 block(s), 1,999 repeated characters
- `SCONST_NJ_AV.I_S14` — 2 block(s), 800 repeated characters

Examples — us_nj_guidance (smallest `act_id`s among the hits):

- `NJ_INS_B_2001_01` — 2 block(s), 799 repeated characters
- `NJ_INS_B_2001_02` — 1 block(s), 400 repeated characters
- `NJ_INS_B_2001_04` — 1 block(s), 400 repeated characters
- `NJ_INS_B_2001_06` — 1 block(s), 399 repeated characters
- `NJ_INS_B_2001_07` — 1 block(s), 400 repeated characters
- `NJ_INS_B_2001_08` — 2 block(s), 799 repeated characters
- `NJ_INS_B_2001_10` — 1 block(s), 400 repeated characters
- `NJ_INS_B_2001_11` — 1 block(s), 400 repeated characters

Examples — us_nj_statutes (smallest `act_id`s among the hits):

- `STATE_NJ_T10_C5_S5-12` — 12 block(s), 4,797 repeated characters
- `STATE_NJ_T10_C5_S5-13` — 1 block(s), 399 repeated characters
- `STATE_NJ_T10_C5_S5-5` — 6 block(s), 2,400 repeated characters
- `STATE_NJ_T10_C5_S5-8` — 1 block(s), 400 repeated characters
- `STATE_NJ_T10_C7_S7-1` — 1 block(s), 400 repeated characters
- `STATE_NJ_T11A_C11_S11-2` — 1 block(s), 400 repeated characters
- `STATE_NJ_T11A_C4_S4-1.3` — 1 block(s), 399 repeated characters
- `STATE_NJ_T11A_C4_S4-1.4` — 1 block(s), 400 repeated characters

Examples — us_nm_constitutions (smallest `act_id`s among the hits):

- `SCONST_NM_AIII_S10` — 8 block(s), 3,198 repeated characters
- `SCONST_NM_AIII_S2` — 1 block(s), 400 repeated characters
- `SCONST_NM_AIV_S1` — 1 block(s), 400 repeated characters
- `SCONST_NM_AIV_S24` — 1 block(s), 400 repeated characters
- `SCONST_NM_AIX_S14` — 4 block(s), 1,600 repeated characters
- `SCONST_NM_AI_S1` — 1 block(s), 400 repeated characters
- `SCONST_NM_AI_S10` — 8 block(s), 3,198 repeated characters
- `SCONST_NM_AI_S14` — 1 block(s), 400 repeated characters

Examples — us_nm_guidance (smallest `act_id`s among the hits):

- `NM_INS_B_2014-002` — 1 block(s), 400 repeated characters
- `NM_INS_B_2014-003` — 1 block(s), 400 repeated characters
- `NM_INS_B_2014-008` — 1 block(s), 400 repeated characters
- `NM_INS_B_2014-016` — 2 block(s), 800 repeated characters
- `NM_INS_B_2014-018` — 1 block(s), 399 repeated characters
- `NM_INS_B_2015-001` — 1 block(s), 400 repeated characters
- `NM_INS_B_2015-002` — 2 block(s), 798 repeated characters
- `NM_INS_B_2015-003` — 2 block(s), 800 repeated characters

Examples — us_nm_regulations (smallest `act_id`s among the hits):

- `SREGS_NM_T1_C10_P11_S10` — 1 block(s), 400 repeated characters
- `SREGS_NM_T1_C10_P11_S8` — 1 block(s), 400 repeated characters
- `SREGS_NM_T1_C10_P12_S10` — 6 block(s), 2,400 repeated characters
- `SREGS_NM_T1_C10_P12_S13` — 5 block(s), 2,000 repeated characters
- `SREGS_NM_T1_C10_P12_S15` — 3 block(s), 1,199 repeated characters
- `SREGS_NM_T1_C10_P12_S16` — 2 block(s), 800 repeated characters
- `SREGS_NM_T1_C10_P12_S17` — 6 block(s), 2,400 repeated characters
- `SREGS_NM_T1_C10_P12_S7` — 3 block(s), 1,199 repeated characters

Examples — us_nm_statutes (smallest `act_id`s among the hits):

- `STATE_NM_C10_A11_S10-11-10.1` — 3 block(s), 1,199 repeated characters
- `STATE_NM_C10_A11_S10-11-116` — 1 block(s), 400 repeated characters
- `STATE_NM_C10_A11_S10-11-118` — 1 block(s), 400 repeated characters
- `STATE_NM_C10_A11_S10-11-130` — 2 block(s), 800 repeated characters
- `STATE_NM_C10_A11_S10-11-14.5` — 2 block(s), 800 repeated characters
- `STATE_NM_C10_A11_S10-11-2` — 2 block(s), 800 repeated characters
- `STATE_NM_C10_A11_S10-11-7` — 2 block(s), 800 repeated characters
- `STATE_NM_C10_A11_S10-11-8` — 2 block(s), 800 repeated characters

Examples — us_nv_constitutions (smallest `act_id`s among the hits):

- `SCONST_NV_A11_S1` — 1 block(s), 400 repeated characters
- `SCONST_NV_A11_S3` — 1 block(s), 399 repeated characters
- `SCONST_NV_A11_S5` — 2 block(s), 800 repeated characters
- `SCONST_NV_A15_S16` — 1 block(s), 400 repeated characters
- `SCONST_NV_A17_S4` — 1 block(s), 399 repeated characters
- `SCONST_NV_A19_S1` — 2 block(s), 799 repeated characters
- `SCONST_NV_A19_S12` — 1 block(s), 400 repeated characters
- `SCONST_NV_A19_S2` — 5 block(s), 1,999 repeated characters

Examples — us_nv_court_rules (smallest `act_id`s among the hits):

- `SRULES_NV_CONDUCT_CWC_R4` — 3 block(s), 1,199 repeated characters
- `SRULES_NV_CONDUCT_CWC_R5` — 1 block(s), 400 repeated characters
- `SRULES_NV_DCR_R12` — 2 block(s), 800 repeated characters
- `SRULES_NV_DCR_R13` — 1 block(s), 400 repeated characters
- `SRULES_NV_DCR_R26` — 3 block(s), 1,199 repeated characters
- `SRULES_NV_DCR_R27` — 5 block(s), 1,999 repeated characters
- `SRULES_NV_EIGHTHDCR_R1_30` — 3 block(s), 1,199 repeated characters
- `SRULES_NV_EIGHTHDCR_R1_44` — 2 block(s), 800 repeated characters

Examples — us_nv_guidance (smallest `act_id`s among the hits):

- `NV_INS_B_00_001` — 2 block(s), 796 repeated characters
- `NV_INS_B_00_002` — 12 block(s), 4,800 repeated characters
- `NV_INS_B_00_003` — 1 block(s), 400 repeated characters
- `NV_INS_B_00_004` — 1 block(s), 400 repeated characters
- `NV_INS_B_01_007` — 2 block(s), 795 repeated characters
- `NV_INS_B_01_009` — 4 block(s), 1,599 repeated characters
- `NV_INS_B_02_000` — 17 block(s), 6,794 repeated characters
- `NV_INS_B_02_003` — 1 block(s), 397 repeated characters

Examples — us_nv_statutes (smallest `act_id`s among the hits):

- `STATE_NV_T10_C111_S111.237` — 1 block(s), 400 repeated characters
- `STATE_NV_T10_C111_S111.2397` — 1 block(s), 399 repeated characters
- `STATE_NV_T10_C111_S111.689` — 1 block(s), 400 repeated characters
- `STATE_NV_T10_C111_S111.779` — 3 block(s), 1,200 repeated characters
- `STATE_NV_T10_C111_S111.781` — 2 block(s), 800 repeated characters
- `STATE_NV_T10_C112_S112.150` — 1 block(s), 400 repeated characters
- `STATE_NV_T10_C113_S113.130` — 1 block(s), 400 repeated characters
- `STATE_NV_T10_C116A_S116A.410` — 1 block(s), 400 repeated characters

Examples — us_ny_constitutions (smallest `act_id`s among the hits):

- `SCONST_NY_AIII_S4` — 8 block(s), 3,198 repeated characters
- `SCONST_NY_AIII_S5` — 3 block(s), 1,199 repeated characters
- `SCONST_NY_AIII_S5-b` — 5 block(s), 1,998 repeated characters
- `SCONST_NY_AIV_S7` — 1 block(s), 400 repeated characters
- `SCONST_NY_AIX_S1` — 1 block(s), 400 repeated characters
- `SCONST_NY_AIX_S2` — 2 block(s), 799 repeated characters
- `SCONST_NY_AI_S6` — 1 block(s), 400 repeated characters
- `SCONST_NY_AI_S9` — 1 block(s), 400 repeated characters

Examples — us_ny_court_rules (smallest `act_id`s among the hits):

- `SRULES_NY_22NYCRR_P100_S100_0` — 4 block(s), 1,599 repeated characters
- `SRULES_NY_22NYCRR_P100_S100_3` — 8 block(s), 3,197 repeated characters
- `SRULES_NY_22NYCRR_P100_S100_4` — 7 block(s), 2,797 repeated characters
- `SRULES_NY_22NYCRR_P100_S100_5` — 6 block(s), 2,400 repeated characters
- `SRULES_NY_22NYCRR_P100_S100_6` — 1 block(s), 400 repeated characters
- `SRULES_NY_22NYCRR_P104_S104_3` — 1 block(s), 400 repeated characters
- `SRULES_NY_22NYCRR_P108_S108_2` — 4 block(s), 1,598 repeated characters
- `SRULES_NY_22NYCRR_P108_S108_3` — 3 block(s), 1,199 repeated characters

Examples — us_ny_guidance (smallest `act_id`s among the hits):

- `NY_CL_C32026_01` — 5 block(s), 2,000 repeated characters
- `NY_CL_C42026_01` — 3 block(s), 1,199 repeated characters
- `NY_CL_CIRCULAR_LETTERS_CL2007_14` — 6 block(s), 2,398 repeated characters
- `NY_CL_CL1924_0509_NN` — 4 block(s), 1,600 repeated characters
- `NY_CL_CL1930_0715_NN` — 1 block(s), 400 repeated characters
- `NY_CL_CL1939_0701_NN` — 3 block(s), 1,198 repeated characters
- `NY_CL_CL1948_NN_10_15` — 1 block(s), 400 repeated characters
- `NY_CL_CL1948_NN_11_01` — 3 block(s), 1,199 repeated characters

Examples — us_ny_statutes (smallest `act_id`s among the hits):

- `STATE_NY_AABC_A1_S3` — 7 block(s), 2,799 repeated characters
- `STATE_NY_AABC_A2_S17` — 6 block(s), 2,400 repeated characters
- `STATE_NY_AABC_A2_S18` — 3 block(s), 1,199 repeated characters
- `STATE_NY_AABC_A3_S30` — 1 block(s), 400 repeated characters
- `STATE_NY_AABC_A3_S31` — 3 block(s), 1,200 repeated characters
- `STATE_NY_AABC_A3_S35` — 2 block(s), 800 repeated characters
- `STATE_NY_AABC_A4-A_S58` — 2 block(s), 800 repeated characters
- `STATE_NY_AABC_A4-A_S58-C` — 4 block(s), 1,600 repeated characters

Examples — us_oh_constitutions (smallest `act_id`s among the hits):

- `SCONST_OH_AII_S11` — 1 block(s), 400 repeated characters
- `SCONST_OH_AII_S1b` — 1 block(s), 400 repeated characters
- `SCONST_OH_AII_S1e` — 1 block(s), 400 repeated characters
- `SCONST_OH_AII_S1g` — 3 block(s), 1,198 repeated characters
- `SCONST_OH_AII_S34a` — 3 block(s), 1,200 repeated characters
- `SCONST_OH_AII_S35` — 1 block(s), 399 repeated characters
- `SCONST_OH_AIV_S2` — 1 block(s), 399 repeated characters
- `SCONST_OH_AIV_S22` — 1 block(s), 400 repeated characters

Examples — us_oh_court_rules (smallest `act_id`s among the hits):

- `SRULES_OH_APP_R10` — 5 block(s), 1,995 repeated characters
- `SRULES_OH_APP_R11_2` — 5 block(s), 1,995 repeated characters
- `SRULES_OH_APP_R12` — 2 block(s), 797 repeated characters
- `SRULES_OH_APP_R13` — 3 block(s), 1,197 repeated characters
- `SRULES_OH_APP_R15` — 1 block(s), 398 repeated characters
- `SRULES_OH_APP_R16` — 1 block(s), 399 repeated characters
- `SRULES_OH_APP_R19` — 1 block(s), 400 repeated characters
- `SRULES_OH_APP_R21` — 2 block(s), 798 repeated characters

Examples — us_oh_guidance (smallest `act_id`s among the hits):

- `OH_INS_B_1988_3` — 3 block(s), 1,200 repeated characters
- `OH_INS_B_1990_6` — 3 block(s), 1,200 repeated characters
- `OH_INS_B_1991_1` — 10 block(s), 3,998 repeated characters
- `OH_INS_B_1991_2` — 1 block(s), 400 repeated characters
- `OH_INS_B_1992_3` — 1 block(s), 400 repeated characters
- `OH_INS_B_1994_2` — 1 block(s), 400 repeated characters
- `OH_INS_B_1995_1` — 1 block(s), 399 repeated characters
- `OH_INS_B_1995_3` — 5 block(s), 1,999 repeated characters

Examples — us_oh_regulations (smallest `act_id`s among the hits):

- `STATE_OH_ADC_011_1_01` — 1 block(s), 400 repeated characters
- `STATE_OH_ADC_101_11_01` — 2 block(s), 800 repeated characters
- `STATE_OH_ADC_101_1_02` — 2 block(s), 800 repeated characters
- `STATE_OH_ADC_101_1_06` — 1 block(s), 399 repeated characters
- `STATE_OH_ADC_101_5_01` — 1 block(s), 399 repeated characters
- `STATE_OH_ADC_101_7_05` — 2 block(s), 800 repeated characters
- `STATE_OH_ADC_101_7_12` — 1 block(s), 400 repeated characters
- `STATE_OH_ADC_102_11_01` — 1 block(s), 400 repeated characters

Examples — us_ok_constitutions (smallest `act_id`s among the hits):

- `SCONST_OK_AII_S18` — 1 block(s), 400 repeated characters
- `SCONST_OK_AII_S34` — 1 block(s), 399 repeated characters
- `SCONST_OK_AII_S37` — 1 block(s), 400 repeated characters
- `SCONST_OK_AIX_S13` — 1 block(s), 400 repeated characters
- `SCONST_OK_AIX_S18` — 2 block(s), 800 repeated characters
- `SCONST_OK_AIX_S20` — 1 block(s), 400 repeated characters
- `SCONST_OK_AIX_S21` — 1 block(s), 399 repeated characters
- `SCONST_OK_AIX_S34` — 1 block(s), 399 repeated characters

Examples — us_ok_guidance (smallest `act_id`s among the hits):

- `OK_INS_B_2014-01` — 1 block(s), 399 repeated characters
- `OK_INS_B_2015-02` — 4 block(s), 1,591 repeated characters
- `OK_INS_B_2015-03` — 1 block(s), 400 repeated characters
- `OK_INS_B_2017-01` — 1 block(s), 397 repeated characters
- `OK_INS_B_2023-10` — 1 block(s), 400 repeated characters
- `OK_INS_B_2024-04` — 5 block(s), 1,998 repeated characters
- `OK_INS_B_2024-05` — 2 block(s), 795 repeated characters
- `OK_INS_B_2024-06` — 2 block(s), 800 repeated characters

Examples — us_ok_statutes (smallest `act_id`s among the hits):

- `STATE_OK_T10A_S10A-1-1-102` — 1 block(s), 400 repeated characters
- `STATE_OK_T10A_S10A-1-1-105v1` — 9 block(s), 3,597 repeated characters
- `STATE_OK_T10A_S10A-1-1-105v2` — 9 block(s), 3,597 repeated characters
- `STATE_OK_T10A_S10A-1-2-101v1` — 2 block(s), 799 repeated characters
- `STATE_OK_T10A_S10A-1-2-101v2` — 2 block(s), 798 repeated characters
- `STATE_OK_T10A_S10A-1-2-101v3` — 2 block(s), 800 repeated characters
- `STATE_OK_T10A_S10A-1-2-102v1` — 1 block(s), 400 repeated characters
- `STATE_OK_T10A_S10A-1-2-102v2` — 1 block(s), 399 repeated characters

Examples — us_or_constitutions (smallest `act_id`s among the hits):

- `SCONST_OR_AIII_S3` — 1 block(s), 400 repeated characters
- `SCONST_OR_AII_S18` — 2 block(s), 800 repeated characters
- `SCONST_OR_AII_S22` — 1 block(s), 400 repeated characters
- `SCONST_OR_AIV_S1` — 3 block(s), 1,200 repeated characters
- `SCONST_OR_AIV_S6-v2` — 4 block(s), 1,600 repeated characters
- `SCONST_OR_AIV_S8` — 2 block(s), 800 repeated characters
- `SCONST_OR_AIX_S14` — 1 block(s), 400 repeated characters
- `SCONST_OR_AIX_S3a` — 1 block(s), 400 repeated characters

Examples — us_or_court_rules (smallest `act_id`s among the hits):

- `SRULES_OR_OCJC_R1_2` — 1 block(s), 398 repeated characters
- `SRULES_OR_OCJC_R1_3` — 2 block(s), 798 repeated characters
- `SRULES_OR_OCJC_R3_10` — 1 block(s), 399 repeated characters
- `SRULES_OR_OCJC_R4_10` — 1 block(s), 399 repeated characters
- `SRULES_OR_ORAP_R10_05` — 1 block(s), 399 repeated characters
- `SRULES_OR_ORAP_R10_10` — 1 block(s), 399 repeated characters
- `SRULES_OR_ORAP_R10_15` — 3 block(s), 1,197 repeated characters
- `SRULES_OR_ORAP_R10_20` — 1 block(s), 399 repeated characters

Examples — us_or_guidance (smallest `act_id`s among the hits):

- `OR_INS_B_1970_04` — 1 block(s), 400 repeated characters
- `OR_INS_B_1994_01` — 1 block(s), 399 repeated characters
- `OR_INS_B_1996_02` — 3 block(s), 1,200 repeated characters
- `OR_INS_B_1996_04` — 1 block(s), 400 repeated characters
- `OR_INS_B_1998_03` — 1 block(s), 400 repeated characters
- `OR_INS_B_2001_01` — 1 block(s), 400 repeated characters
- `OR_INS_B_2002_03` — 2 block(s), 799 repeated characters
- `OR_INS_B_2003_02` — 9 block(s), 3,596 repeated characters

Examples — us_or_statutes (smallest `act_id`s among the hits):

- `STATE_OR_T10_C100_S100.005` — 3 block(s), 1,200 repeated characters
- `STATE_OR_T10_C100_S100.020` — 1 block(s), 400 repeated characters
- `STATE_OR_T10_C100_S100.023` — 1 block(s), 400 repeated characters
- `STATE_OR_T10_C100_S100.105` — 4 block(s), 1,600 repeated characters
- `STATE_OR_T10_C100_S100.110` — 2 block(s), 799 repeated characters
- `STATE_OR_T10_C100_S100.115` — 2 block(s), 798 repeated characters
- `STATE_OR_T10_C100_S100.116` — 2 block(s), 799 repeated characters
- `STATE_OR_T10_C100_S100.117` — 1 block(s), 400 repeated characters

Examples — us_pa_constitutions (smallest `act_id`s among the hits):

- `SCONST_PA_AII_S17` — 3 block(s), 1,200 repeated characters
- `SCONST_PA_AIV_S8` — 1 block(s), 400 repeated characters
- `SCONST_PA_AIX_S12` — 1 block(s), 400 repeated characters
- `SCONST_PA_AVIII_S11` — 1 block(s), 400 repeated characters
- `SCONST_PA_AVIII_S17` — 1 block(s), 400 repeated characters
- `SCONST_PA_AVIII_S2` — 3 block(s), 1,200 repeated characters
- `SCONST_PA_AVIII_S7` — 2 block(s), 800 repeated characters
- `SCONST_PA_AV_S13` — 1 block(s), 400 repeated characters

Examples — us_pa_court_rules (smallest `act_id`s among the hits):

- `SRULES_PA_T201_R102` — 1 block(s), 400 repeated characters
- `SRULES_PA_T201_R103` — 9 block(s), 3,597 repeated characters
- `SRULES_PA_T201_R107` — 2 block(s), 800 repeated characters
- `SRULES_PA_T201_R1901` — 4 block(s), 1,600 repeated characters
- `SRULES_PA_T201_R1904` — 1 block(s), 400 repeated characters
- `SRULES_PA_T201_R1905` — 2 block(s), 799 repeated characters
- `SRULES_PA_T201_R1910` — 6 block(s), 2,400 repeated characters
- `SRULES_PA_T201_R1922` — 5 block(s), 1,999 repeated characters

Examples — us_pa_statutes (smallest `act_id`s among the hits):

- `STATE_PA_T11_C118_S11804.1` — 1 block(s), 400 repeated characters
- `STATE_PA_T11_C124_S12402.1` — 2 block(s), 799 repeated characters
- `STATE_PA_T11_C125_S12522` — 1 block(s), 400 repeated characters
- `STATE_PA_T11_C125_S12531` — 1 block(s), 400 repeated characters
- `STATE_PA_T11_C129_S12975` — 1 block(s), 400 repeated characters
- `STATE_PA_T11_C132_S13240` — 1 block(s), 399 repeated characters
- `STATE_PA_T11_C143_S14303` — 1 block(s), 400 repeated characters
- `STATE_PA_T11_C143_S14322` — 1 block(s), 400 repeated characters

Examples — us_pr_constitutions (smallest `act_id`s among the hits):

- `SCONST_PR_AIII_S7` — 2 block(s), 799 repeated characters
- `SCONST_PR_AVIII_S1` — 1 block(s), 400 repeated characters
- `SCONST_PR_AVI_S2` — 2 block(s), 799 repeated characters

Examples — us_pr_court_rules (smallest `act_id`s among the hits):

- `SRULES_PR_CEJ_R15` — 2 block(s), 800 repeated characters
- `SRULES_PR_CEJ_R20` — 1 block(s), 399 repeated characters
- `SRULES_PR_CEJ_R26` — 1 block(s), 399 repeated characters
- `SRULES_PR_CEJ_R35` — 1 block(s), 398 repeated characters
- `SRULES_PR_CEP_R24` — 1 block(s), 399 repeated characters
- `SRULES_PR_CEP_R33` — 1 block(s), 399 repeated characters
- `SRULES_PR_CEP_R36` — 2 block(s), 798 repeated characters
- `SRULES_PR_CEP_R38` — 2 block(s), 798 repeated characters

Examples — us_pr_guidance (smallest `act_id`s among the hits):

- `PR_INS_B_CC-1-176-58` — 2 block(s), 799 repeated characters
- `PR_INS_B_CC-11-170-57` — 1 block(s), 400 repeated characters
- `PR_INS_B_CC-11-171-57` — 2 block(s), 799 repeated characters
- `PR_INS_B_CC-11-173-57` — 1 block(s), 400 repeated characters
- `PR_INS_B_CC-2-146-57` — 1 block(s), 400 repeated characters
- `PR_INS_B_CC-2-183-58` — 2 block(s), 799 repeated characters
- `PR_INS_B_CC-2-540-73` — 2 block(s), 800 repeated characters
- `PR_INS_B_CC-2007-1769-ES` — 2 block(s), 798 repeated characters

Examples — us_ri_constitutions (smallest `act_id`s among the hits):

- `SCONST_RI_AIV_S1` — 2 block(s), 800 repeated characters

Examples — us_ri_court_rules (smallest `act_id`s among the hits):

- `SRULES_RI_DISTCIV_R1` — 4 block(s), 1,597 repeated characters
- `SRULES_RI_DISTCIV_R11` — 1 block(s), 400 repeated characters
- `SRULES_RI_DISTCIV_R12` — 4 block(s), 1,595 repeated characters
- `SRULES_RI_DISTCIV_R13` — 1 block(s), 399 repeated characters
- `SRULES_RI_DISTCIV_R14` — 1 block(s), 400 repeated characters
- `SRULES_RI_DISTCIV_R15` — 2 block(s), 798 repeated characters
- `SRULES_RI_DISTCIV_R17` — 1 block(s), 399 repeated characters
- `SRULES_RI_DISTCIV_R19` — 1 block(s), 398 repeated characters

Examples — us_ri_guidance (smallest `act_id`s among the hits):

- `RI_INS_B_2002_11` — 1 block(s), 399 repeated characters
- `RI_INS_B_2002_13` — 1 block(s), 400 repeated characters
- `RI_INS_B_2002_16` — 5 block(s), 1,993 repeated characters
- `RI_INS_B_2002_3` — 2 block(s), 798 repeated characters
- `RI_INS_B_2003_18` — 3 block(s), 1,200 repeated characters
- `RI_INS_B_2003_2` — 3 block(s), 1,196 repeated characters
- `RI_INS_B_2004_11` — 2 block(s), 798 repeated characters
- `RI_INS_B_2005_12` — 5 block(s), 1,999 repeated characters

Examples — us_ri_statutes (smallest `act_id`s among the hits):

- `STATE_RI_T10_C10-21_S10-21-2` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-17_S11-17-13` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-18_S11-18-34` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-19_S11-19-24` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-19_S11-19-31` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-19_S11-19-39` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-27_S11-27-19` — 1 block(s), 400 repeated characters
- `STATE_RI_T11_C11-37_S11-37-8.2.1` — 1 block(s), 399 repeated characters

Examples — us_sc_constitutions (smallest `act_id`s among the hits):

- `SCONST_SC_AIII_S34` — 1 block(s), 400 repeated characters
- `SCONST_SC_AIII_S36` — 2 block(s), 800 repeated characters
- `SCONST_SC_AIV_S12` — 1 block(s), 400 repeated characters
- `SCONST_SC_AI_S24` — 2 block(s), 800 repeated characters
- `SCONST_SC_AI_S34` — 1 block(s), 400 repeated characters
- `SCONST_SC_AI_S36` — 2 block(s), 800 repeated characters
- `SCONST_SC_AXVII_S11` — 1 block(s), 400 repeated characters
- `SCONST_SC_AXVII_S7-v2` — 4 block(s), 1,600 repeated characters

Examples — us_sc_court_rules (smallest `act_id`s among the hits):

- `SRULES_SC_SCACR_407_R1_0` — 7 block(s), 2,800 repeated characters
- `SRULES_SC_SCACR_407_R1_1` — 2 block(s), 800 repeated characters
- `SRULES_SC_SCACR_407_R1_10` — 4 block(s), 1,600 repeated characters
- `SRULES_SC_SCACR_407_R1_11` — 5 block(s), 1,999 repeated characters
- `SRULES_SC_SCACR_407_R1_12` — 2 block(s), 800 repeated characters
- `SRULES_SC_SCACR_407_R1_13` — 8 block(s), 3,199 repeated characters
- `SRULES_SC_SCACR_407_R1_14` — 5 block(s), 1,998 repeated characters
- `SRULES_SC_SCACR_407_R1_15` — 9 block(s), 3,598 repeated characters

Examples — us_sc_guidance (smallest `act_id`s among the hits):

- `SC_INS_B_1999-01` — 7 block(s), 2,795 repeated characters
- `SC_INS_B_1999-02` — 3 block(s), 1,197 repeated characters
- `SC_INS_B_1999-04` — 2 block(s), 800 repeated characters
- `SC_INS_B_1999-05` — 1 block(s), 400 repeated characters
- `SC_INS_B_1999-06` — 27 block(s), 10,790 repeated characters
- `SC_INS_B_2000-03` — 5 block(s), 1,995 repeated characters
- `SC_INS_B_2000-06` — 1 block(s), 400 repeated characters
- `SC_INS_B_2000-09` — 1 block(s), 396 repeated characters

Examples — us_sc_regulations (smallest `act_id`s among the hits):

- `STATE_SC_CODEREGS_100_1` — 3 block(s), 1,199 repeated characters
- `STATE_SC_CODEREGS_100_10` — 1 block(s), 400 repeated characters
- `STATE_SC_CODEREGS_100_4` — 16 block(s), 6,396 repeated characters
- `STATE_SC_CODEREGS_100_6` — 1 block(s), 399 repeated characters
- `STATE_SC_CODEREGS_100_8` — 3 block(s), 1,200 repeated characters
- `STATE_SC_CODEREGS_101_07` — 7 block(s), 2,799 repeated characters
- `STATE_SC_CODEREGS_103_102` — 5 block(s), 2,000 repeated characters
- `STATE_SC_CODEREGS_103_133` — 16 block(s), 6,395 repeated characters

Examples — us_sc_statutes (smallest `act_id`s among the hits):

- `STATE_SC_T10_C1_S10-1-161` — 1 block(s), 400 repeated characters
- `STATE_SC_T10_C1_S10-1-168` — 3 block(s), 1,200 repeated characters
- `STATE_SC_T10_C1_S10-1-179` — 1 block(s), 400 repeated characters
- `STATE_SC_T10_C1_S10-1-185` — 1 block(s), 400 repeated characters
- `STATE_SC_T11_C11_A1_S11-11-156` — 3 block(s), 1,200 repeated characters
- `STATE_SC_T11_C11_A1_S11-11-170` — 1 block(s), 400 repeated characters
- `STATE_SC_T11_C11_A3_S11-11-320` — 1 block(s), 400 repeated characters
- `STATE_SC_T11_C11_A5_S11-11-410` — 1 block(s), 400 repeated characters

Examples — us_sd_constitutions (smallest `act_id`s among the hits):

- `SCONST_SD_AIII_S0` — 13 block(s), 5,199 repeated characters
- `SCONST_SD_AIII_S25` — 1 block(s), 400 repeated characters
- `SCONST_SD_AIV_S0` — 5 block(s), 2,000 repeated characters
- `SCONST_SD_AIV_S3` — 1 block(s), 399 repeated characters
- `SCONST_SD_AIX_S0` — 1 block(s), 399 repeated characters
- `SCONST_SD_AVIII_S0` — 8 block(s), 3,200 repeated characters
- `SCONST_SD_AVI_S0` — 9 block(s), 3,599 repeated characters
- `SCONST_SD_AVI_S29` — 4 block(s), 1,600 repeated characters

Examples — us_sd_guidance (smallest `act_id`s among the hits):

- `SD_INS_B_1998_05` — 1 block(s), 399 repeated characters
- `SD_INS_B_2007_01` — 1 block(s), 400 repeated characters
- `SD_INS_B_2010_04` — 1 block(s), 400 repeated characters
- `SD_INS_B_2012_01` — 1 block(s), 399 repeated characters
- `SD_INS_B_2012_02` — 1 block(s), 400 repeated characters
- `SD_INS_B_2012_03` — 1 block(s), 400 repeated characters
- `SD_INS_B_2012_06` — 1 block(s), 400 repeated characters
- `SD_INS_B_2013_03` — 2 block(s), 799 repeated characters

Examples — us_sd_regulations (smallest `act_id`s among the hits):

- `STATE_SD_ARSD_T02_A01_C02_S01` — 1 block(s), 399 repeated characters
- `STATE_SD_ARSD_T02_A01_C06_S03` — 1 block(s), 400 repeated characters
- `STATE_SD_ARSD_T02_A01_C13_S01` — 1 block(s), 400 repeated characters
- `STATE_SD_ARSD_T02_A03_C01_S01` — 4 block(s), 1,600 repeated characters
- `STATE_SD_ARSD_T02_A03_C01_S02` — 1 block(s), 400 repeated characters
- `STATE_SD_ARSD_T02_A03_C01_S03` — 1 block(s), 400 repeated characters
- `STATE_SD_ARSD_T02_A03_C01_S05` — 2 block(s), 800 repeated characters
- `STATE_SD_ARSD_T02_A06_C01_S01` — 1 block(s), 400 repeated characters

Examples — us_sd_statutes (smallest `act_id`s among the hits):

- `STATE_SD_T10_C43_S10-43-1` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C44_S10-44-2` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C45D_S10-45D-1` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C45_S10-45-1` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C45_S10-45-1.17` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C45_S10-45-13` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C46_S10-46-1` — 1 block(s), 400 repeated characters
- `STATE_SD_T10_C46_S10-46-1.2` — 1 block(s), 400 repeated characters

Examples — us_tn_constitutions (smallest `act_id`s among the hits):

- `SCONST_TN_AIII_S12` — 1 block(s), 399 repeated characters
- `SCONST_TN_AIII_S18` — 1 block(s), 400 repeated characters
- `SCONST_TN_AII_S28` — 4 block(s), 1,599 repeated characters
- `SCONST_TN_AI_S31` — 1 block(s), 399 repeated characters
- `SCONST_TN_AXI_S3` — 1 block(s), 400 repeated characters
- `SCONST_TN_AXI_S9` — 2 block(s), 800 repeated characters
- `SCONST_TN_AX_S4` — 2 block(s), 800 repeated characters

Examples — us_tn_court_rules (smallest `act_id`s among the hits):

- `SRULES_TN_TNCTAPPR_R11` — 1 block(s), 399 repeated characters
- `SRULES_TN_TNCTAPPR_R13` — 1 block(s), 400 repeated characters
- `SRULES_TN_TNCTAPPR_R15` — 3 block(s), 1,198 repeated characters
- `SRULES_TN_TNCTAPPR_R4` — 1 block(s), 400 repeated characters
- `SRULES_TN_TNCTAPPR_R5` — 1 block(s), 400 repeated characters
- `SRULES_TN_TNCTAPPR_R6` — 1 block(s), 399 repeated characters
- `SRULES_TN_TNCTAPPR_R7` — 1 block(s), 400 repeated characters
- `SRULES_TN_TNCTCRIMAPPR_R19` — 2 block(s), 800 repeated characters

Examples — us_tn_guidance (smallest `act_id`s among the hits):

- `TN_INS_B_19850808_8_5_85` — 2 block(s), 799 repeated characters
- `TN_INS_B_19880506_5_6_88` — 2 block(s), 798 repeated characters
- `TN_INS_B_19880901_9_1_88` — 1 block(s), 400 repeated characters
- `TN_INS_B_19880901_9_1_88A` — 6 block(s), 2,397 repeated characters
- `TN_INS_B_19880901_9_1_88B` — 1 block(s), 400 repeated characters
- `TN_INS_B_19880901_9_1_88I` — 1 block(s), 400 repeated characters
- `TN_INS_B_19881011_10_11_88` — 1 block(s), 400 repeated characters
- `TN_INS_B_19890110_1_10_89` — 1 block(s), 398 repeated characters

Examples — us_tn_statutes (smallest `act_id`s among the hits):

- `STATE_TN_T10_C1_S10-1-104` — 1 block(s), 400 repeated characters
- `STATE_TN_T10_C3_S10-3-103` — 2 block(s), 799 repeated characters
- `STATE_TN_T10_C7_S10-7-121` — 1 block(s), 400 repeated characters
- `STATE_TN_T10_C7_S10-7-123` — 2 block(s), 799 repeated characters
- `STATE_TN_T10_C7_S10-7-301` — 2 block(s), 800 repeated characters
- `STATE_TN_T10_C7_S10-7-303` — 1 block(s), 400 repeated characters
- `STATE_TN_T10_C7_S10-7-404` — 4 block(s), 1,599 repeated characters
- `STATE_TN_T10_C7_S10-7-406` — 1 block(s), 400 repeated characters

Examples — us_tx_constitutions (smallest `act_id`s among the hits):

- `SCONST_TX_A16_S16` — 1 block(s), 400 repeated characters
- `SCONST_TX_A16_S20` — 1 block(s), 400 repeated characters
- `SCONST_TX_A16_S40` — 2 block(s), 800 repeated characters
- `SCONST_TX_A16_S44` — 1 block(s), 400 repeated characters
- `SCONST_TX_A16_S50` — 25 block(s), 9,995 repeated characters
- `SCONST_TX_A16_S59` — 4 block(s), 1,599 repeated characters
- `SCONST_TX_A16_S6` — 1 block(s), 399 repeated characters
- `SCONST_TX_A16_S61` — 1 block(s), 400 repeated characters

Examples — us_tx_court_rules (smallest `act_id`s among the hits):

- `SRULES_TX_APPELLATE_R1` — 4 block(s), 1,598 repeated characters
- `SRULES_TX_APPELLATE_R10` — 4 block(s), 1,596 repeated characters
- `SRULES_TX_APPELLATE_R10_5` — 1 block(s), 400 repeated characters
- `SRULES_TX_APPELLATE_R12` — 2 block(s), 798 repeated characters
- `SRULES_TX_APPELLATE_R13` — 2 block(s), 796 repeated characters
- `SRULES_TX_APPELLATE_R14` — 1 block(s), 399 repeated characters
- `SRULES_TX_APPELLATE_R18` — 5 block(s), 1,995 repeated characters
- `SRULES_TX_APPELLATE_R2` — 39 block(s), 15,561 repeated characters

Examples — us_tx_guidance (smallest `act_id`s among the hits):

- `TX_INS_B_0001_00` — 1 block(s), 400 repeated characters
- `TX_INS_B_0001_01` — 2 block(s), 799 repeated characters
- `TX_INS_B_0001_02` — 3 block(s), 1,199 repeated characters
- `TX_INS_B_0001_03` — 3 block(s), 1,200 repeated characters
- `TX_INS_B_0001_04` — 3 block(s), 1,200 repeated characters
- `TX_INS_B_0001_05` — 3 block(s), 1,200 repeated characters
- `TX_INS_B_0001_06` — 3 block(s), 1,199 repeated characters
- `TX_INS_B_0001_14` — 1 block(s), 400 repeated characters

Examples — us_tx_statutes (smallest `act_id`s among the hits):

- `STATE_TX_Cag_C12_S12.0029` — 1 block(s), 400 repeated characters
- `STATE_TX_Cag_C12_S12.020` — 2 block(s), 800 repeated characters
- `STATE_TX_Cag_C12_S12.039` — 1 block(s), 399 repeated characters
- `STATE_TX_Cag_C12_S12.040` — 1 block(s), 398 repeated characters
- `STATE_TX_Cag_C12_S12.042` — 1 block(s), 400 repeated characters
- `STATE_TX_Cag_C14_S14.015` — 1 block(s), 400 repeated characters
- `STATE_TX_Cag_C14_S14.082` — 1 block(s), 400 repeated characters
- `STATE_TX_Cag_C161_S161.148` — 1 block(s), 400 repeated characters

Examples — us_ut_constitutions (smallest `act_id`s among the hits):

- `SCONST_UT_AIII_S0` — 1 block(s), 400 repeated characters
- `SCONST_UT_AVII_S10` — 2 block(s), 798 repeated characters
- `SCONST_UT_AVII_S11` — 4 block(s), 1,599 repeated characters
- `SCONST_UT_AVII_S8` — 1 block(s), 400 repeated characters
- `SCONST_UT_AVI_S1-v2` — 1 block(s), 400 repeated characters
- `SCONST_UT_AVI_S2` — 1 block(s), 400 repeated characters
- `SCONST_UT_AXIII_S3` — 2 block(s), 797 repeated characters
- `SCONST_UT_AXIII_S5` — 2 block(s), 799 repeated characters

Examples — us_ut_court_rules (smallest `act_id`s among the hits):

- `SRULES_UT_ADR_R101` — 2 block(s), 799 repeated characters
- `SRULES_UT_ADR_R102` — 7 block(s), 2,798 repeated characters
- `SRULES_UT_ADR_R104` — 9 block(s), 3,599 repeated characters
- `SRULES_UT_SCRP_R1_101` — 2 block(s), 799 repeated characters
- `SRULES_UT_SCRP_R1_102` — 1 block(s), 400 repeated characters
- `SRULES_UT_SCRP_R1_103` — 1 block(s), 400 repeated characters
- `SRULES_UT_SCRP_R1_105` — 1 block(s), 400 repeated characters
- `SRULES_UT_SCRP_R1_107` — 2 block(s), 800 repeated characters

Examples — us_ut_guidance (smallest `act_id`s among the hits):

- `UT_INS_B_1987-06` — 1 block(s), 400 repeated characters
- `UT_INS_B_1990-03` — 1 block(s), 399 repeated characters
- `UT_INS_B_1990-04` — 3 block(s), 1,200 repeated characters
- `UT_INS_B_1991-02` — 1 block(s), 400 repeated characters
- `UT_INS_B_1992-01` — 1 block(s), 400 repeated characters
- `UT_INS_B_1992-07` — 2 block(s), 800 repeated characters
- `UT_INS_B_1994-01` — 2 block(s), 800 repeated characters
- `UT_INS_B_1994-02` — 2 block(s), 800 repeated characters

Examples — us_va_constitutions (smallest `act_id`s among the hits):

- `SCONST_VA_AII_S1` — 1 block(s), 400 repeated characters
- `SCONST_VA_AII_S2` — 1 block(s), 399 repeated characters
- `SCONST_VA_AII_S6` — 1 block(s), 400 repeated characters
- `SCONST_VA_AII_S6-A` — 4 block(s), 1,599 repeated characters
- `SCONST_VA_AIV_S11` — 1 block(s), 400 repeated characters
- `SCONST_VA_AIV_S6` — 1 block(s), 399 repeated characters
- `SCONST_VA_AI_S11` — 1 block(s), 400 repeated characters
- `SCONST_VA_AVI_S1` — 1 block(s), 400 repeated characters

Examples — us_va_court_rules (smallest `act_id`s among the hits):

- `SRULES_VA_P11_R11_2` — 1 block(s), 399 repeated characters
- `SRULES_VA_P11_R11_4` — 2 block(s), 798 repeated characters
- `SRULES_VA_P11_R11_5` — 1 block(s), 399 repeated characters
- `SRULES_VA_P1A_R1A_1` — 12 block(s), 4,795 repeated characters
- `SRULES_VA_P1A_R1A_4` — 6 block(s), 2,393 repeated characters
- `SRULES_VA_P1A_R1A_5` — 11 block(s), 4,388 repeated characters
- `SRULES_VA_P1A_R1A_6` — 6 block(s), 2,394 repeated characters
- `SRULES_VA_P1A_R1A_7` — 6 block(s), 2,394 repeated characters

Examples — us_va_guidance (smallest `act_id`s among the hits):

- `VA_INS_AL_1979-20` — 1 block(s), 400 repeated characters
- `VA_INS_AL_1979-21` — 13 block(s), 5,198 repeated characters
- `VA_INS_AL_1981-09` — 1 block(s), 400 repeated characters
- `VA_INS_AL_1981-10` — 1 block(s), 400 repeated characters
- `VA_INS_AL_1981-14` — 1 block(s), 400 repeated characters
- `VA_INS_AL_1982-10` — 3 block(s), 1,200 repeated characters
- `VA_INS_AL_1987-04` — 4 block(s), 1,598 repeated characters
- `VA_INS_AL_1990-15` — 1 block(s), 399 repeated characters

Examples — us_va_regulations (smallest `act_id`s among the hits):

- `STATE_VA_ADC_10_5_10_10` — 5 block(s), 1,999 repeated characters
- `STATE_VA_ADC_10_5_110_20` — 3 block(s), 1,200 repeated characters
- `STATE_VA_ADC_10_5_110_40` — 3 block(s), 1,200 repeated characters
- `STATE_VA_ADC_10_5_120_10` — 1 block(s), 400 repeated characters
- `STATE_VA_ADC_10_5_120_40` — 2 block(s), 800 repeated characters
- `STATE_VA_ADC_10_5_120_70` — 1 block(s), 400 repeated characters
- `STATE_VA_ADC_10_5_140_10` — 1 block(s), 400 repeated characters
- `STATE_VA_ADC_10_5_160_10` — 5 block(s), 2,000 repeated characters

Examples — us_va_statutes (smallest `act_id`s among the hits):

- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2202` — 1 block(s), 400 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2202.4` — 1 block(s), 399 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2202.5` — 1 block(s), 400 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2211.1` — 1 block(s), 400 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2211.2` — 1 block(s), 400 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2212` — 1 block(s), 400 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2213` — 1 block(s), 400 repeated characters
- `STATE_VA_T10.1_SIII_C22_A1_S10.1-2213.1` — 1 block(s), 400 repeated characters

Examples — us_vt_constitutions (smallest `act_id`s among the hits):

- `SCONST_VT_A21_S0` — 23 block(s), 9,192 repeated characters
- `SCONST_VT_AII_S20` — 1 block(s), 400 repeated characters
- `SCONST_VT_AI_S0` — 2 block(s), 800 repeated characters

Examples — us_vt_guidance (smallest `act_id`s among the hits):

- `VT_INS_B_101_19981001` — 1 block(s), 400 repeated characters
- `VT_INS_B_102_19930805` — 32 block(s), 12,787 repeated characters
- `VT_INS_B_102_19990315` — 1 block(s), 400 repeated characters
- `VT_INS_B_104_19990603` — 6 block(s), 2,397 repeated characters
- `VT_INS_B_105_19940701` — 2 block(s), 800 repeated characters
- `VT_INS_B_105_19990804` — 5 block(s), 1,997 repeated characters
- `VT_INS_B_106_19961018` — 7 block(s), 2,800 repeated characters
- `VT_INS_B_107_19950710` — 5 block(s), 1,998 repeated characters

Examples — us_vt_statutes (smallest `act_id`s among the hits):

- `STATE_VT_T10APPENDIX_C1_S10` — 4 block(s), 1,600 repeated characters
- `STATE_VT_T10APPENDIX_C1_S11` — 5 block(s), 1,997 repeated characters
- `STATE_VT_T10APPENDIX_C1_S12` — 2 block(s), 800 repeated characters
- `STATE_VT_T10APPENDIX_C1_S15` — 3 block(s), 1,199 repeated characters
- `STATE_VT_T10APPENDIX_C1_S15b` — 1 block(s), 400 repeated characters
- `STATE_VT_T10APPENDIX_C1_S18` — 2 block(s), 800 repeated characters
- `STATE_VT_T10APPENDIX_C1_S19` — 7 block(s), 2,800 repeated characters
- `STATE_VT_T10APPENDIX_C1_S19a` — 3 block(s), 1,198 repeated characters

Examples — us_wa_constitutions (smallest `act_id`s among the hits):

- `SCONST_WA_AIII_S10` — 1 block(s), 399 repeated characters
- `SCONST_WA_AIII_S12` — 2 block(s), 800 repeated characters
- `SCONST_WA_AII_S1` — 10 block(s), 3,998 repeated characters
- `SCONST_WA_AII_S12` — 1 block(s), 400 repeated characters
- `SCONST_WA_AII_S15` — 4 block(s), 1,599 repeated characters
- `SCONST_WA_AII_S33` — 1 block(s), 398 repeated characters
- `SCONST_WA_AII_S42` — 2 block(s), 800 repeated characters
- `SCONST_WA_AII_S43` — 5 block(s), 2,000 repeated characters

Examples — us_wa_court_rules (smallest `act_id`s among the hits):

- `SRULES_WA_APR_R1` — 3 block(s), 1,196 repeated characters
- `SRULES_WA_APR_R11` — 16 block(s), 6,380 repeated characters
- `SRULES_WA_APR_R12` — 8 block(s), 3,192 repeated characters
- `SRULES_WA_APR_R13` — 1 block(s), 399 repeated characters
- `SRULES_WA_APR_R14` — 4 block(s), 1,596 repeated characters
- `SRULES_WA_APR_R15` — 3 block(s), 1,196 repeated characters
- `SRULES_WA_APR_R15P` — 16 block(s), 6,384 repeated characters
- `SRULES_WA_APR_R17` — 1 block(s), 399 repeated characters

Examples — us_wa_guidance (smallest `act_id`s among the hits):

- `WA_OIC_EO_25_01` — 2 block(s), 800 repeated characters
- `WA_OIC_EO_26_02` — 5 block(s), 1,998 repeated characters
- `WA_OIC_EO_WSR_26_16_059` — 5 block(s), 1,995 repeated characters
- `WA_OIC_MEMO_AETNA_PROVIDENCE_BRIEFING_MEMO_AUG_2024` — 1 block(s), 399 repeated characters
- `WA_OIC_TAA_2015_01` — 1 block(s), 400 repeated characters
- `WA_OIC_TAA_2016_01` — 5 block(s), 1,998 repeated characters
- `WA_OIC_TAA_2017_01` — 1 block(s), 400 repeated characters
- `WA_OIC_TAA_2017_01a` — 2 block(s), 800 repeated characters

Examples — us_wa_regulations (smallest `act_id`s among the hits):

- `STATE_WA_ADC_100_100_020` — 3 block(s), 1,199 repeated characters
- `STATE_WA_ADC_100_100_030` — 1 block(s), 400 repeated characters
- `STATE_WA_ADC_100_100_040` — 2 block(s), 799 repeated characters
- `STATE_WA_ADC_100_100_050` — 1 block(s), 400 repeated characters
- `STATE_WA_ADC_100_100_052` — 1 block(s), 400 repeated characters
- `STATE_WA_ADC_100_100_070` — 9 block(s), 3,597 repeated characters
- `STATE_WA_ADC_100_100_080` — 3 block(s), 1,198 repeated characters
- `STATE_WA_ADC_106_116_901` — 1 block(s), 400 repeated characters

Examples — us_wa_statutes (smallest `act_id`s among the hits):

- `STATE_WA_T10_C01_S160` — 1 block(s), 400 repeated characters
- `STATE_WA_T10_C05_S020` — 1 block(s), 400 repeated characters
- `STATE_WA_T10_C101_S010` — 1 block(s), 399 repeated characters
- `STATE_WA_T10_C101_S080` — 1 block(s), 400 repeated characters
- `STATE_WA_T10_C101_S272` — 1 block(s), 400 repeated characters
- `STATE_WA_T10_C105_S010` — 2 block(s), 800 repeated characters
- `STATE_WA_T10_C116_S060` — 1 block(s), 400 repeated characters
- `STATE_WA_T10_C120_S020` — 1 block(s), 400 repeated characters

Examples — us_wi_constitutions (smallest `act_id`s among the hits):

- `SCONST_WI_AIII_S0` — 1 block(s), 400 repeated characters
- `SCONST_WI_AII_S0` — 1 block(s), 400 repeated characters
- `SCONST_WI_AIV_S0` — 8 block(s), 3,198 repeated characters
- `SCONST_WI_AIV_S24` — 5 block(s), 1,999 repeated characters
- `SCONST_WI_AI_S0` — 6 block(s), 2,398 repeated characters
- `SCONST_WI_AI_S8` — 2 block(s), 800 repeated characters
- `SCONST_WI_AI_S9m` — 3 block(s), 1,199 repeated characters
- `SCONST_WI_AVIII_S0` — 4 block(s), 1,599 repeated characters

Examples — us_wi_court_rules (smallest `act_id`s among the hits):

- `SRULES_WI_SCR10_R10_03` — 15 block(s), 5,989 repeated characters
- `SRULES_WI_SCR10_R10_04` — 2 block(s), 797 repeated characters
- `SRULES_WI_SCR10_R10_05` — 8 block(s), 3,184 repeated characters
- `SRULES_WI_SCR10_R10_06` — 1 block(s), 400 repeated characters
- `SRULES_WI_SCR10_R10_08` — 3 block(s), 1,194 repeated characters
- `SRULES_WI_SCR10_R10_14` — 47 block(s), 18,761 repeated characters
- `SRULES_WI_SCR11_R11_04` — 1 block(s), 399 repeated characters
- `SRULES_WI_SCR12_R12_02` — 3 block(s), 1,195 repeated characters

Examples — us_wi_guidance (smallest `act_id`s among the hits):

- `WI_INS_B_19960606_INS3455` — 5 block(s), 1,999 repeated characters
- `WI_INS_B_19960628_LIMITSLIAB` — 3 block(s), 1,200 repeated characters
- `WI_INS_B_19960703_RESCISSIONS` — 7 block(s), 2,796 repeated characters
- `WI_INS_B_19960815_FORMFILING` — 8 block(s), 3,198 repeated characters
- `WI_INS_B_19960930_CREDITRATES` — 1 block(s), 399 repeated characters
- `WI_INS_B_19970314_ACT289W2` — 1 block(s), 399 repeated characters
- `WI_INS_B_19970616_CREDITRPTS` — 1 block(s), 400 repeated characters
- `WI_INS_B_19970715_ACT11` — 3 block(s), 1,199 repeated characters

Examples — us_wi_regulations (smallest `act_id`s among the hits):

- `STATE_WI_ADC_AB_1_02` — 1 block(s), 400 repeated characters
- `STATE_WI_ADC_AB_1_16` — 2 block(s), 799 repeated characters
- `STATE_WI_ADC_ATCP_100_12` — 2 block(s), 800 repeated characters
- `STATE_WI_ADC_ATCP_100_13` — 1 block(s), 400 repeated characters
- `STATE_WI_ADC_ATCP_100_135` — 6 block(s), 2,399 repeated characters
- `STATE_WI_ADC_ATCP_100_16` — 2 block(s), 800 repeated characters
- `STATE_WI_ADC_ATCP_100_20` — 1 block(s), 400 repeated characters
- `STATE_WI_ADC_ATCP_100_30` — 3 block(s), 1,200 repeated characters

Examples — us_wi_statutes (smallest `act_id`s among the hits):

- `STATE_WI_C100_S100.171` — 2 block(s), 799 repeated characters
- `STATE_WI_C100_S100.173` — 1 block(s), 400 repeated characters
- `STATE_WI_C100_S100.174` — 1 block(s), 400 repeated characters
- `STATE_WI_C100_S100.175` — 1 block(s), 400 repeated characters
- `STATE_WI_C100_S100.18` — 5 block(s), 1,999 repeated characters
- `STATE_WI_C100_S100.195` — 1 block(s), 400 repeated characters
- `STATE_WI_C100_S100.197` — 1 block(s), 398 repeated characters
- `STATE_WI_C100_S100.20` — 1 block(s), 400 repeated characters

Examples — us_wv_constitutions (smallest `act_id`s among the hits):

- `SCONST_WV_AIII_S0` — 2 block(s), 800 repeated characters
- `SCONST_WV_AIV_S0` — 3 block(s), 1,200 repeated characters
- `SCONST_WV_AIX_S11` — 1 block(s), 400 repeated characters
- `SCONST_WV_AVIII_S10` — 2 block(s), 800 repeated characters
- `SCONST_WV_AVIII_S3` — 1 block(s), 399 repeated characters
- `SCONST_WV_AVIII_S5` — 1 block(s), 400 repeated characters
- `SCONST_WV_AVIII_S6` — 1 block(s), 400 repeated characters
- `SCONST_WV_AVIII_S7` — 2 block(s), 800 repeated characters

Examples — us_wv_court_rules (smallest `act_id`s among the hits):

- `SRULES_WV_CJC_R2_11` — 3 block(s), 1,199 repeated characters
- `SRULES_WV_CJC_R2_15` — 1 block(s), 400 repeated characters
- `SRULES_WV_CJC_R2_3` — 1 block(s), 400 repeated characters
- `SRULES_WV_CJC_R2_9` — 3 block(s), 1,200 repeated characters
- `SRULES_WV_CJC_R3_1` — 2 block(s), 800 repeated characters
- `SRULES_WV_CJC_R3_13` — 4 block(s), 1,599 repeated characters
- `SRULES_WV_CJC_R3_14` — 2 block(s), 800 repeated characters
- `SRULES_WV_CJC_R3_15` — 1 block(s), 400 repeated characters

Examples — us_wv_guidance (smallest `act_id`s among the hits):

- `WV_INS_B_20-01` — 4 block(s), 1,596 repeated characters
- `WV_INS_B_20-02` — 4 block(s), 1,596 repeated characters
- `WV_INS_B_20-03` — 2 block(s), 796 repeated characters
- `WV_INS_B_20-04A` — 2 block(s), 800 repeated characters
- `WV_INS_B_20-05` — 2 block(s), 799 repeated characters
- `WV_INS_B_20-06A` — 1 block(s), 400 repeated characters
- `WV_INS_B_20-07` — 9 block(s), 3,595 repeated characters
- `WV_INS_B_20-08` — 2 block(s), 800 repeated characters

Examples — us_wv_statutes (smallest `act_id`s among the hits):

- `STATE_WV_C10_A1A_S1` — 3 block(s), 1,200 repeated characters
- `STATE_WV_C10_A2_S4A` — 1 block(s), 400 repeated characters
- `STATE_WV_C10_A3_S2` — 2 block(s), 800 repeated characters
- `STATE_WV_C11A_A3_S2` — 1 block(s), 399 repeated characters
- `STATE_WV_C11A_A3_S45` — 1 block(s), 400 repeated characters
- `STATE_WV_C11A_A3_S56` — 1 block(s), 400 repeated characters
- `STATE_WV_C11B_A1_S8` — 1 block(s), 400 repeated characters
- `STATE_WV_C11B_A2_S20` — 2 block(s), 800 repeated characters

Examples — us_wy_constitutions (smallest `act_id`s among the hits):

- `SCONST_WY_A10_S4` — 1 block(s), 400 repeated characters
- `SCONST_WY_A13_S1` — 2 block(s), 800 repeated characters
- `SCONST_WY_A3_S27` — 1 block(s), 400 repeated characters
- `SCONST_WY_A3_S52` — 2 block(s), 800 repeated characters
- `SCONST_WY_A5_S6` — 2 block(s), 799 repeated characters

Examples — us_wy_court_rules (smallest `act_id`s among the hits):

- `SRULES_WY_BYLABAR_R3` — 4 block(s), 1,600 repeated characters
- `SRULES_WY_BYLABAR_R5` — 7 block(s), 2,798 repeated characters
- `SRULES_WY_CODEJUDICOND_R2_11` — 3 block(s), 1,198 repeated characters
- `SRULES_WY_CODEJUDICOND_R2_15` — 1 block(s), 400 repeated characters
- `SRULES_WY_CODEJUDICOND_R2_3` — 1 block(s), 400 repeated characters
- `SRULES_WY_CODEJUDICOND_R2_6` — 1 block(s), 400 repeated characters
- `SRULES_WY_CODEJUDICOND_R2_9` — 2 block(s), 800 repeated characters
- `SRULES_WY_CODEJUDICOND_R3_1` — 1 block(s), 400 repeated characters

Examples — us_wy_guidance (smallest `act_id`s among the hits):

- `WY_INS_B_1_2026_20260122` — 2 block(s), 800 repeated characters
- `WY_INS_M_10_2021_20211012` — 2 block(s), 799 repeated characters
- `WY_INS_M_10_2022_20221007` — 1 block(s), 400 repeated characters
- `WY_INS_M_10_2024_20241018` — 1 block(s), 400 repeated characters
- `WY_INS_M_11_2021_20211118` — 1 block(s), 400 repeated characters
- `WY_INS_M_11_2023_20231128` — 1 block(s), 400 repeated characters
- `WY_INS_M_12_2020_20201207` — 12 block(s), 4,796 repeated characters
- `WY_INS_M_12_2022_20221223` — 1 block(s), 399 repeated characters

Examples — us_wy_statutes (smallest `act_id`s among the hits):

- `STATE_WY_T10_C3_S10-3-201` — 1 block(s), 399 repeated characters
- `STATE_WY_T10_C3_S10-3-601` — 1 block(s), 400 repeated characters
- `STATE_WY_T11_C12_S11-12-101` — 1 block(s), 400 repeated characters
- `STATE_WY_T11_C13_S11-13-102` — 1 block(s), 400 repeated characters
- `STATE_WY_T11_C14_S11-14-103` — 1 block(s), 400 repeated characters
- `STATE_WY_T11_C16_S11-16-117` — 1 block(s), 400 repeated characters
- `STATE_WY_T11_C16_S11-16-122` — 1 block(s), 400 repeated characters
- `STATE_WY_T11_C17_S11-17-207` — 1 block(s), 400 repeated characters

## Damage that reached the extracted fields

Rows whose own `cross_references_usc` names a US Code title that does not exist (outside 1-54) — the corruption propagating out of the text into the dataset's structured columns.

| file | rows with an impossible cross-reference title |
|---|---:|
| us_ak_constitutions | 0 |
| us_ak_court_rules | 0 |
| us_ak_guidance | 0 |
| us_ak_statutes | 0 |
| us_al_constitutions | 0 |
| us_al_court_rules | 0 |
| us_al_guidance | 0 |
| us_al_statutes | 0 |
| us_ar_constitutions | 0 |
| us_ar_guidance | 0 |
| us_ar_statutes | 0 |
| us_az_constitutions | 0 |
| us_az_court_rules | 0 |
| us_az_guidance | 0 |
| us_az_statutes | 0 |
| us_ca_constitutions | 0 |
| us_ca_court_rules | 0 |
| us_ca_guidance | 0 |
| us_ca_statutes | 0 |
| us_co_constitutions | 0 |
| us_co_regulations | 0 |
| us_co_statutes | 0 |
| us_ct_constitutions | 0 |
| us_ct_court_rules | 0 |
| us_ct_guidance | 0 |
| us_ct_statutes | 0 |
| us_dc_administrative_guidance | 0 |
| us_dc_court_rules | 0 |
| us_dc_guidance | 0 |
| us_dc_statutes | 0 |
| us_de_constitutions | 0 |
| us_de_court_rules | 0 |
| us_de_guidance | 0 |
| us_de_regulations | 0 |
| us_de_statutes | 0 |
| us_federal_administrative_guidance | 0 |
| us_federal_constitutions | 0 |
| us_federal_court_rules | 0 |
| us_federal_enforcement_action | 0 |
| us_federal_executive_order | 0 |
| us_federal_faq | 0 |
| us_federal_guidance | 0 |
| us_federal_guideline | 0 |
| us_federal_irs_announcement | 0 |
| us_federal_irs_notice | 0 |
| us_federal_irs_rev_proc | 0 |
| us_federal_irs_rev_rul | 0 |
| us_federal_memorandum | 0 |
| us_federal_presidential_document | 0 |
| us_federal_proclamation | 0 |
| us_federal_regulations | 0 |
| us_federal_ruling | 0 |
| us_federal_statutes | 1 |
| us_federal_treaty | 0 |
| us_fl_constitutions | 0 |
| us_fl_court_rules | 0 |
| us_fl_guidance | 0 |
| us_fl_statutes | 0 |
| us_ga_constitutions | 0 |
| us_ga_court_rules | 0 |
| us_ga_guidance | 0 |
| us_hi_constitutions | 0 |
| us_hi_court_rules | 0 |
| us_hi_guidance | 0 |
| us_hi_statutes | 0 |
| us_ia_constitutions | 0 |
| us_ia_court_rules | 0 |
| us_ia_guidance | 0 |
| us_ia_statutes | 0 |
| us_id_constitutions | 0 |
| us_id_court_rules | 0 |
| us_id_guidance | 0 |
| us_id_regulations | 0 |
| us_id_statutes | 0 |
| us_il_constitutions | 0 |
| us_il_court_rules | 0 |
| us_il_guidance | 0 |
| us_il_regulations | 0 |
| us_il_statutes | 0 |
| us_in_constitutions | 0 |
| us_in_court_rules | 0 |
| us_in_guidance | 0 |
| us_in_statutes | 0 |
| us_ks_constitutions | 0 |
| us_ks_court_rules | 0 |
| us_ks_guidance | 0 |
| us_ks_statutes | 0 |
| us_ky_constitutions | 0 |
| us_ky_guidance | 0 |
| us_ky_regulations | 0 |
| us_ky_statutes | 0 |
| us_la_constitutions | 0 |
| us_la_court_rules | 0 |
| us_la_statutes | 0 |
| us_ma_constitutions | 0 |
| us_ma_court_rules | 0 |
| us_ma_guidance | 0 |
| us_ma_statutes | 0 |
| us_md_constitutions | 0 |
| us_md_court_rules | 0 |
| us_md_guidance | 0 |
| us_md_regulations | 0 |
| us_md_statutes | 0 |
| us_me_constitutions | 0 |
| us_me_court_rules | 0 |
| us_me_guidance | 0 |
| us_me_regulations | 0 |
| us_me_statutes | 0 |
| us_mi_constitutions | 0 |
| us_mi_court_rules | 0 |
| us_mi_guidance | 0 |
| us_mi_statutes | 0 |
| us_mn_constitutions | 0 |
| us_mn_court_rules | 0 |
| us_mn_guidance | 0 |
| us_mn_regulations | 0 |
| us_mn_statutes | 0 |
| us_mo_constitutions | 0 |
| us_mo_guidance | 0 |
| us_mo_statutes | 0 |
| us_ms_constitutions | 0 |
| us_ms_court_rules | 0 |
| us_ms_guidance | 0 |
| us_ms_statutes | 0 |
| us_mt_constitutions | 0 |
| us_mt_court_rules | 0 |
| us_mt_guidance | 0 |
| us_mt_statutes | 0 |
| us_nc_constitutions | 0 |
| us_nc_court_rules | 0 |
| us_nc_guidance | 0 |
| us_nd_constitutions | 0 |
| us_nd_court_rules | 0 |
| us_nd_guidance | 0 |
| us_nd_statutes | 0 |
| us_ne_constitutions | 0 |
| us_ne_court_rules | 0 |
| us_ne_guidance | 0 |
| us_ne_statutes | 0 |
| us_nh_constitutions | 0 |
| us_nh_court_rules | 0 |
| us_nh_guidance | 0 |
| us_nh_statutes | 0 |
| us_nj_constitutions | 0 |
| us_nj_guidance | 0 |
| us_nj_statutes | 0 |
| us_nm_constitutions | 0 |
| us_nm_guidance | 0 |
| us_nm_regulations | 0 |
| us_nm_statutes | 0 |
| us_nv_constitutions | 0 |
| us_nv_court_rules | 0 |
| us_nv_guidance | 0 |
| us_nv_statutes | 0 |
| us_ny_constitutions | 0 |
| us_ny_court_rules | 0 |
| us_ny_guidance | 0 |
| us_ny_statutes | 0 |
| us_oh_constitutions | 0 |
| us_oh_court_rules | 0 |
| us_oh_guidance | 0 |
| us_oh_regulations | 0 |
| us_oh_statutes | 0 |
| us_ok_constitutions | 0 |
| us_ok_guidance | 0 |
| us_ok_statutes | 0 |
| us_or_constitutions | 0 |
| us_or_court_rules | 0 |
| us_or_guidance | 0 |
| us_or_statutes | 0 |
| us_pa_constitutions | 0 |
| us_pa_court_rules | 0 |
| us_pa_statutes | 0 |
| us_pr_constitutions | 0 |
| us_pr_court_rules | 0 |
| us_pr_guidance | 0 |
| us_pr_statutes | 0 |
| us_ri_constitutions | 0 |
| us_ri_court_rules | 0 |
| us_ri_guidance | 0 |
| us_ri_statutes | 0 |
| us_sc_constitutions | 0 |
| us_sc_court_rules | 0 |
| us_sc_guidance | 0 |
| us_sc_regulations | 0 |
| us_sc_statutes | 0 |
| us_sd_constitutions | 0 |
| us_sd_guidance | 0 |
| us_sd_regulations | 0 |
| us_sd_statutes | 0 |
| us_tn_constitutions | 0 |
| us_tn_court_rules | 0 |
| us_tn_guidance | 0 |
| us_tn_statutes | 0 |
| us_tx_constitutions | 0 |
| us_tx_court_rules | 0 |
| us_tx_guidance | 0 |
| us_tx_regulations | 0 |
| us_tx_statutes | 0 |
| us_ut_constitutions | 0 |
| us_ut_court_rules | 0 |
| us_ut_guidance | 0 |
| us_ut_statutes | 0 |
| us_va_constitutions | 0 |
| us_va_court_rules | 0 |
| us_va_guidance | 0 |
| us_va_regulations | 0 |
| us_va_statutes | 0 |
| us_vt_constitutions | 0 |
| us_vt_guidance | 0 |
| us_vt_statutes | 0 |
| us_wa_constitutions | 0 |
| us_wa_court_rules | 0 |
| us_wa_guidance | 0 |
| us_wa_regulations | 0 |
| us_wa_statutes | 0 |
| us_wi_constitutions | 0 |
| us_wi_court_rules | 0 |
| us_wi_guidance | 0 |
| us_wi_regulations | 0 |
| us_wi_statutes | 0 |
| us_wv_constitutions | 0 |
| us_wv_court_rules | 0 |
| us_wv_guidance | 0 |
| us_wv_statutes | 0 |
| us_wy_constitutions | 0 |
| us_wy_court_rules | 0 |
| us_wy_guidance | 0 |
| us_wy_statutes | 0 |

## Samples — us_ak_guidance

Truncated heads (each begins mid-word):

- `AK_INS_B_1990-03_ADDENDUM` — `ins  
 
ADDENDUM TO BULLETIN 90-3 
TO: ALL SURPLUS LINES BROKERS, RESIDENT AND NONRESIDE…`

## Samples — us_al_statutes

Truncated heads (each begins mid-word):

- `STATE_AL_T17_C8_S17-8-6` — `ion official to attend at the hour of 7:00 a.m., the precinct election officials as may …`
- `STATE_AL_T41_C4_S41-4-66` — `ficer shall establish and maintain and post on the state’s website a statewide database …`
- `STATE_AL_T45_C36_S45-36-232.30` — `a) A person who has been conditionally released pursuant to Section 45-36-232.28 and who…`
- `STATE_AL_T45_C37_S45-37-150.05` — `a) Upon special application submitted by a qualified organization licensed pursuant to S…`
- `STATE_AL_T45_C56_S45-56-70.03` — `for the general election in 2028, the members of the Randolph County Commission represen…`
- `STATE_AL_T8_C19J_S8-19J-3` — `app store provider shall do all of the following when an individual is determined to be …`
- `STATE_AL_T8_C19K_S8-19K-3` — `app store provider shall do all of the following when an individual is determined to be …`

## Samples — us_ar_guidance

Truncated heads (each begins mid-word):

- `AR_INS_B_1979-13` — `ee 
74, 
W. H. L. Woodyard Ill 
Insurance Commissioner 
ARKANSAS 
INSURANCE 
DEPARTMENT …`
- `AR_INS_B_1981-14` — `et 
• 
• 
NC STi 
r. 
rf 
W. H. L. Woodyard Ill
Insurance Commissioner 
BULLETIN NO. 14-…`
- `AR_INS_B_1982-16` — `s
• 
Insurance Commissioner 
BULLETIN NO. 16-82 
.1%, t 
0 
4 
7 
ARKANSAS 
INSURANCE 
D…`
- `AR_INS_B_1993-14` — `of, Sr 
ARKANSAS 
INSURANCE 
DEPARTMENT 
400 University Tower Building 
1123 South U niv…`

## Samples — us_ar_statutes

Truncated heads (each begins mid-word):

- `STATE_AR_T11_C10_S2_S11-10-210` — `stitute employment, then none of the services of the individual for the period shall be …`
- `STATE_AR_T24_C2_S3_S24-2-302` — `nded by Act 2019, No. 910,§ 2361, eff. 7/1/2019. Amended by Act 2019, No. 910,§ 2360, ef…`
- `STATE_AR_T24_C7_S4_S24-7-401` — `or exceed the value of the proposed employer contribution increase. (d) The value of cos…`
- `STATE_AR_T25_C16_S7_S25-16-714` — `n dollars ($25,000,000). (e) An aggregate contingency fee shall not exceed fifty million…`
- `STATE_AR_T3_C1_S3-1-103` — `d for scientific, chemical, mechanical, industrial, medicinal, or culinary purposes or f…`

## Samples — us_az_court_rules

Truncated heads (each begins mid-word):

- `SRULES_AZ_AREVICTP_R10` — `a. Upon request, a party must provide to the other party prior to the hearing or trial: …`
- `SRULES_AZ_AREVICTP_R11` — `a. In General. All proceedings in eviction actions shall be recorded, either through a r…`
- `SRULES_AZ_AREVICTP_R12` — `a. When an action is called for trial by jury, the jury panel shall be assembled. Voir d…`
- `SRULES_AZ_AREVICTP_R13` — `a. Items to Review. Except for stipulated judgments entered pursuant to Rule 13(b)(4), i…`
- `SRULES_AZ_AREVICTP_R15` — `a. Motions to Set Aside Judgments, Orders, or Proceedings. Either party may file a motio…`
- `SRULES_AZ_AREVICTP_R17` — `a. General. Appeals from a lower court to the superior court shall be taken in the manne…`
- `SRULES_AZ_AREVICTP_R18` — `a. “Eviction” or “eviction action” as used herein shall mean forcible detainer actions a…`
- `SRULES_AZ_AREVICTP_R19` — `a. If a plaintiff is entitled to rent, late charges, court costs or attorney fees in a d…`

## Samples — us_ca_guidance

Truncated heads (each begins mid-word):

- `CA_INS_N_1405-001-2` — `stewarf 
~ title guaranty company 
ROBERT M. CAVALLARO 
Vice-President 
Region Eliieflel…`

## Samples — us_ca_statutes

Truncated heads (each begins mid-word):

- `STATE_CA_Cccp_P2_T10_C10_S871.1` — `as used in this chapter, “good faith improver” means:

(a) A person who makes an improve…`
- `STATE_CA_Cedc_T1_D1_P6_C2_A13.1_S8320` — `region.

(2) To the extent funds are available in the Budget Act of 2023, existing grant…`
- `STATE_CA_Cedc_T1_D1_P6_C2_A22.6_S8484.8` — `to submit annual budget reports, and the department may withhold funds in subsequent yea…`
- `STATE_CA_Cedc_T2_D4_P28_C6.1_A4.5_S52064.5` — `d pursuant to subparagraph (A) due to any of the events described in subdivision (a) of …`
- `STATE_CA_Cedc_T3_D5_P42_C2_A22_S70022` — `t of 1965, as amended (20 U.S.C. Sec. 1087mm et seq.), and applicable rules and regulati…`
- `STATE_CA_Clab_D1_C1_S62.5` — `excess of payment of administrative expenses incurred by the director for the insurance …`

## Samples — us_co_constitutions

Truncated heads (each begins mid-word):

- `SCONST_CO_AIV_S13` — `irst named member of the general assembly listed in subsection (7) of this section who i…`
- `SCONST_CO_AVIII_S5` — `of higher education, whether established by this constitution or by law, shall have the …`
- `SCONST_CO_AVII_S8` — `ity, city and county, or town; such bonds, certificates or other obligations may be made…`
- `SCONST_CO_AV_S44.1` — `section (4) of this section, an elected political party official above the precinct leve…`
- `SCONST_CO_AXVIII_S2` — `rates without profit to its members and which has been in existence continuously for a p…`
- `SCONST_CO_AXXI_S2` — `an ten days after such notice is mailed. All hearings shall be before the officer with w…`
- `SCONST_CO_AXXI_S3` — `cross (X), his vote for or against such recall. On such ballots, under each question, th…`
- `SCONST_CO_AXXI_S4` — `m shall be performed by the lieutenant-governor; and if the secretary of state is sought…`

## Samples — us_co_regulations

Truncated heads (each begins mid-word):

- `STATE_CO_CCR_1_CCR_301_47` — `eff. 05/30/2017
1 CCR 301-47
[Editor’s Notes follow the text of the rules at the end of …`
- `STATE_CO_CCR_1_CCR_301_67` — `eff. 07/30/2012
1 CCR 301-67
[Editor’s Notes follow the text of the rules at the end of …`
- `STATE_CO_CCR_4_CCR_723_14` — `eff. 04/01/2006
4 CCR 723-14
[Editor’s Notes follow the text of the rules at the end of …`
- `STATE_CO_CCR_8_CCR_1202_3` — `eff. 11/30/2017
8 CCR 1202-3
[Editor’s Notes follow the text of the rules at the end of …`
- `STATE_CO_CCR_8_CCR_1302_1` — `effective 11/30/03
8 CCR 1302-1
[Editor’s Notes follow the text of the rules at the end …`
- `STATE_CO_CCR_8_CCR_1507_13` — `eff. 03/01/2004
8 CCR 1507-13
[Editor’s Notes follow the text of the rules at the end of…`

## Samples — us_ct_constitutions

Truncated heads (each begins mid-word):

- `SCONST_CT_AIII_S6` — `a. The assembly and senatorial districts as now established by law shall continue until …`
- `SCONST_CT_AVII_S3` — `of article sixth of the constitution is amended to read as follows: The general assembly…`
- `SCONST_CT_AV_S20` — `of article first of the constitution is amended to read as follows: No person shall be d…`
- `SCONST_CT_AXIII_S9` — `of article sixth of the constitution is repealed. Adopted November 26, 1980.…`
- `SCONST_CT_AXII_S6` — `of article third of the constitution is amended to read as follows: SEC. 6. a. The assem…`
- `SCONST_CT_AXVII_S8` — `of the article first of the constitution is amended to read as follows: In all criminal …`
- `SCONST_CT_AXXII_S18` — `of article fourth of the constitution is amended to read as follows: a. In case of the d…`
- `SCONST_CT_AXXIV_S5` — `of article sixth of the constitution is amended to read as follows: In all elections of …`

## Samples — us_ct_court_rules

Truncated heads (each begins mid-word):

- `SRULES_CT_EVID_R10_3` — `of Contents
The original of a writing, recording or photo- 
graph is not required, and o…`
- `SRULES_CT_EVID_R4_11` — `ual Conduct in Criminal Prosecutions
‘‘In any prosecution for sexual assault under 
sect…`
- `SRULES_CT_EVID_R4_12` — `tim’s Sexual Behavior in Civil Proceedings 
Involving Alleged Sexual Misconduct
‘‘(a) As…`
- `SRULES_CT_EVID_R6_5` — `est
The credibility of a witness may be impeached 
by evidence showing bias for, prejudi…`
- `SRULES_CT_EVID_R6_6` — `duct of Witness
(a) Opinion and reputation evidence of char- 
acter. The credibility of …`
- `SRULES_CT_EVID_R6_8` — `sequent Examinations; Leading Questions
(a) Scope of cross-examination and subse- 
quent…`
- `SRULES_CT_EVID_R7_4` — `of Opinion Testimony by Experts; Hypothet- 
ical Questions
(a) Opinion testimony by expe…`
- `SRULES_CT_EVID_R8_4` — `and Photographic Copies: Availability of 
Declarant Immaterial
‘‘(a) [Business records a…`

## Samples — us_ct_guidance

Truncated heads (each begins mid-word):

- `CT_INS_FS_37` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_FS_38` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_FS_39` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_HC_108` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_HC_109` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_HC_116` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_HC_81_23` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
An Equal Opportunity Employer 
 
S…`
- `CT_INS_HC_81_24` — `www.ct.gov/cid 
P.O. Box 816 Hartford, CT 06142-0816 
Affirmative Action/Equal Employmen…`

## Samples — us_dc_court_rules

Truncated heads (each begins mid-word):

- `SRULES_DC_SUPPROBPRE2022_R232_VPRE20220822` — `todian or to require the custodian to give appropriate bond. 
(a) Petition for Order to …`
- `SRULES_DC_SUPPROBPRE2022_R308_VPRE20220822` — `ers and visitors. 
(a) Compensation by order of the Court. Any visitor, attorney, examin…`
- `SRULES_DC_SUPPROBPRE2022_R321_VPRE20220822` — `ship or conservatorship. 
(a) Petition. 
A general proceeding is initiated by filing a p…`
- `SRULES_DC_SUPPROBPRE2022_R322_VPRE20220822` — `guardian or conservator and for resolution of disputes. 
(a) Applicability. 
This Rule a…`
- `SRULES_DC_SUPPROBPRE2022_R350_VPRE20220822` — `peared or detained person. 
(a) Applicability of Rule. 
This Rule applies to proceedings…`
- `SRULES_DC_SUPPROBPRE2022_R63_VPRE20220822` — `cal to 28 U.S.C. § 144.

Decedents’ Estates After January 1, 1981.…`

## Samples — us_de_court_rules

Truncated heads (each begins mid-word):

- `SRULES_DE_DELRPC_R1_7` — `may give consent under this Rule. See Rule 1.0(e) for the definition of 
informed consen…`
- `SRULES_DE_DELRPC_R3_1` — `believes it to be true on the basis of a reasonably diligent inquiry. There 
are circums…`
- `SRULES_DE_DELRPC_R5_7` — `must be met when the lawyer accepts an interest in the client’s business or 
other nonmo…`
- `SRULES_DE_DELRPC_R7_1` — `occasionally cross) the dividing line between accurate representations and 
those that a…`

## Samples — us_de_regulations

Truncated heads (each begins mid-word):

- `STATE_DE_ADC_T16_14000` — `a single, streamlined application and supplemental forms to collect the additional infor…`
- `STATE_DE_ADC_T16_15000` — `in error;
pending a hearing if the agency’s action is upheld and the Medicaid provided i…`
- `STATE_DE_ADC_T16_20000` — `property taxes
interest payments on mortgage
incidental repairs
advertising for tenants
…`
- `STATE_DE_ADC_T16_2102` — `prevent the onset of an illness, condition, injury, or disability;
reduce or ameliorate …`
- `STATE_DE_ADC_T16_3210` — `family visits to the facility and flexibility in accommodating such visits,
the pediatri…`
- `STATE_DE_ADC_T16_3330` — `an Emergency Plan that is based on a Risk Assessment and incorporates an all hazards app…`
- `STATE_DE_ADC_T16_60000` — `department of health and social services
Division of Social Services
Division of Social …`
- `STATE_DE_ADC_T16_7000` — `vidence of intentional violation (e.g., information intentionally omitted from applicati…`

## Samples — us_federal_guidance

Truncated heads (each begins mid-word):

- `BIS_AO_20071119` — `r-~"""
\~i
..,.dI.l
UNITED STATES DEPARTMENT OF COMMERCE
Bureau af Industry and Security…`
- `CPSC_AO_120` — `kuz--~ 
CONSUMER PRODUCT SAFETY COMMISSION 
WASHINGTON, D.C. 20207 
Fred 
A. Manuele 
M …`
- `CPSC_AO_130` — `cnNs,::-.IER PRODUCT SAFETY CO.\lMlSSION 
WASHINGTON, D.C. '.?0'.?07 
AUG 5 
1974 
Hr. C…`
- `CPSC_AO_154` — `l!ouora.hle 
Jack 
~':!) 
llo!l.Se of Rep-rese..~tat:i ves 
Washington9 
DC 20515 
Dear …`
- `CPSC_AO_157` — `l 
f 
Mr. Robert 
K. Brewer 
BSP Enterprises 
Highway 
69 North 
P. o. Box 686 
Tyler, 
…`
- `CPSC_AO_270` — `r .:.) ~ r. ~"': ~. - 1 
-· .. 
'-..I~ 
". 
~ .. '-". 
~ 
-L;m,11e11t,; 
Processed 
U.S.…`
- `CPSC_AO_299` — `w
I
.-
’
U.S.
CCNS~ME~=i
PpGCuCT
SA=ETv
CcMMISSiCN
0
--.--
WASWINCTGN,
2C2C7
--y=>.-
MY …`
- `CPSC_AO_322` — `it.W~~f2t~~ 
-==='=-
41' :JJ.2 
-WITH PORnONI 
IBIOVED: ---
U.S. CONSUMER 
PRODUCT SAFET…`

## Samples — us_federal_guideline

Truncated heads (each begins mid-word):

- `USSG_S2B5.4` — `tion with §2B5.3 effective November 1, 1993 (amendment 481). * * * * * 6. MOTOR VEHICLE …`
- `USSG_S2C1.4` — `amended effective November 1, 1998 (amendment 588), was deleted by consolidation with §2…`
- `USSG_S2E1.5` — `ber 1, 1989 (amendment 145), was deleted by consolidation with §§2B3.1, 2B3.2, 2B3.3, an…`
- `USSG_S2E5.2` — `ber 1, 1987, and amended effective June 15, 1988 (amendment 28), November 1, 1989 (amend…`
- `USSG_S2G1.2` — `effective November 1, 1987, and amended effective November 1, 1989 (amendments 159 and 1…`
- `USSG_S2K1.7` — `ment 188), and amended effective November 1, 1990 (amendment 332), was deleted by consol…`
- `USSG_S2K3.1` — `was deleted by consolidation with §2Q1.2 effective November 1, 1993 (amendment 481).…`
- `USSG_S2L1.3` — `deleted effective November 1, 1989 (amendment 194). * * * * * 2. NATURALIZATION AND PASS…`

## Samples — us_federal_regulations

Truncated heads (each begins mid-word):

- `CFR_T10_P10_S10_11` — `ited States or any State or any subdivisions thereof by unlawful means, or which advocat…`
- `CFR_T10_P26_S26_205` — `al evolutions; and holdovers for interviews needed for event investigations. (2) Within-…`
- `CFR_T10_P2_S2_202` — `ublic health, safety, or interest so requires or that the violation or conduct causing t…`
- `CFR_T10_P2_S2_202` — `e requirements, the requirements of § 52.63 of this chapter must be followed, unless the…`
- `CFR_T10_P2_S2_390` — `piled by a criminal law enforcement authority in the course of a criminal investigation,…`
- `CFR_T10_P31_S31_5` — `ng the radioactive materials, its shielding or containment, are performed: (i) In accord…`
- `CFR_T10_P51_S51_4` — `and transmission lines);
(H) Procurement or fabrication of components or portions of the…`
- `CFR_T10_P54_S54_17` — `possess Restricted Data or classified National Security Information until the individual…`

UI chrome in the body:

- `CFR_T10_P1040_S1040_1` — `Link to an amendment published at 90 FR 20782, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_102` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_12` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_13` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_14` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_5` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_6` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_72` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`

## Samples — us_federal_ruling

Truncated heads (each begins mid-word):

- `FINCEN_FIN2013R003` — `www.fincen.gov 
 
 
 
FIN-2013-R003  
Issued:     November 13, 2013  
Subject:   Applica…`
- `FINCEN_FIN2014R010` — `www.fincen.gov 
 
 
 RULING 
 
FIN-2014-R010  
Issued: September 24, 2014  
Subject: Adm…`

## Samples — us_federal_statutes

Truncated heads (each begins mid-word):

- `USC_T15_C2A_S77aa` — `schedule a

(1) The name under which the issuer is doing or intends to do business;

(2)…`

## Samples — us_federal_treaty

Truncated heads (each begins mid-word):

- `TREATY_US_NORWAY_TE` — `tially similar to those covered by the 
convention. 
The convention may be extended 
pur…`
- `TREATY_US_POLAND_TE` — `with respect to the special reference to 
third country investors. 
The provisions for a…`

## Samples — us_fl_court_rules

Truncated heads (each begins mid-word):

- `SRULES_FL_CIVIL_R1_720` — `entative having full authority to settle” shall mean
the final decision maker with respe…`
- `SRULES_FL_CIVIL_R1_900` — `ourthouse in………., Florida, on
.....(date)....., at ......(a.m./p.m.), to testify in this…`

## Samples — us_fl_statutes

Truncated heads (each begins mid-word):

- `STATE_FL_TXXX_C409_PIII_S409.912` — `s to purchase durable medical equipment and other goods is less expensive to the Medicai…`
- `STATE_FL_TX_C121_PII_S121.591` — `nse account are payable upon a proper application, not to include earnings thereon, as p…`

## Samples — us_ga_court_rules

Truncated heads (each begins mid-word):

- `SRULES_GA_JURY_R1` — `dissemination, and technological improvements of inclusive statewide and county master j…`
- `SRULES_GA_JURY_R2` — `accordance with the process and business rules set forth in the Appendix to this Rule.…`
- `SRULES_GA_JURY_R3` — `a. Each county master jury list should be no less than 85% inclusive of the number of ci…`
- `SRULES_GA_JURY_R4` — `a. Upon completion of the statewide and county master jury lists, the Council or its lis…`
- `SRULES_GA_JURY_R5` — `a. A county master jury list may be subjected to additions, deferrals, excusals, and ina…`
- `SRULES_GA_JURY_R7` — `opinion on any issue regarding jury selection, the operation of the Rule, or compliance …`
- `SRULES_GA_SCT_R100` — `following limits shall apply to the practice of law by recent law school 
graduates who …`
- `SRULES_GA_SCT_R101` — `admission under Part XVI shall expire in the following ways: 

(1) If not terminated or …`

## Samples — us_ga_guidance

Truncated heads (each begins mid-word):

- `GA_INS_B_2021_EX_10` — `v. 1  6/2021
Surprise Billing Arbitration Application Form
The Georgia Legislature enact…`

## Samples — us_hi_constitutions

Truncated heads (each begins mid-word):

- `SCONST_HI_AIV_S2` — `the commission or a council shall be filled by the initial selecting authority within fi…`

## Samples — us_hi_court_rules

Truncated heads (each begins mid-word):

- `SRULES_HI_LFRR_R10_1` — `the Supreme Court

of the State of Hawai‘i

Effective June 22, 1994

The Judiciary

Stat…`

## Samples — us_hi_statutes

Truncated heads (each begins mid-word):

- `STATE_HI_D1_T18_C309_S309-1` — `or other similar public or private nonprofit corporations. The department of budget and …`
- `STATE_HI_D1_T21_C393_S393-6` — `prohibited. If an individual is concurrently a regular employee of two or more employers…`
- `STATE_HI_D3_T31_C577_S577-23` — `responsibility, penalty. Any parent, guardian, or other person having the care, custody,…`

## Samples — us_ia_court_rules

Truncated heads (each begins mid-word):

- `SRULES_IA_CH10_R10_1` — `section 598.21(8A), the district court makes a finding that the parent awarded physical …`
- `SRULES_IA_CH10_R10_2` — `the parent might apply for return of the bond after a reasonable period of compliance wi…`
- `SRULES_IA_CH10_R10_3` — `court may schedule a hearing to determine whether the parent with physical care has cont…`
- `SRULES_IA_CH10_R10_4` — `has continued to interfere with visitation, it may order the bond forfeited to the other…`
- `SRULES_IA_CH12_R12_10` — `should allow the respondent’s attorney to present evidence and argument prior to the jud…`
- `SRULES_IA_CH12_R12_11` — `attorney is afforded no opportunity to present evidence and argument prior to the determ…`
- `SRULES_IA_CH12_R12_12` — `with a copy of the examination report filed pursuant to Iowa Code section 229.10(2), as …`
- `SRULES_IA_CH12_R12_13` — `the examination as required by Iowa Code section 229.10(2) on the form designated for us…`

## Samples — us_id_constitutions

Truncated heads (each begins mid-word):

- `SCONST_ID_AIII_S20` — `b. Games that award only additional play.…`
- `SCONST_ID_AVIII_S3D` — `provided that any revenue bonds, indebtedness or liability shall be payable solely from …`

## Samples — us_id_court_rules

Truncated heads (each begins mid-word):

- `SRULES_ID_IRCP_R37_1` — `of Civil Cases.
(a)   Definitions of Mediation.
Mediation under this Rule is the process…`

## Samples — us_id_regulations

Truncated heads (each begins mid-word):

- `STATE_ID_IDAPA_18_04_10_001` — `a. Except as specifically provided in Sections 046, 051, 066, and 077, this chapter appl…`

## Samples — us_id_statutes

Truncated heads (each begins mid-word):

- `STATE_ID_T16_C16_S16-1619` — `s.

(7)(a) The court shall also inquire regarding:

(i) Whether there is reason to belie…`
- `STATE_ID_T16_C16_S16-1648` — `division of the state;

(ii) Any agency of the state or of a political subdivision of th…`
- `STATE_ID_T18_C13_S18-1359` — `wages, pay or compensation of such appointee or employee is to be paid out of public fun…`
- `STATE_ID_T18_C33_S18-3302K` — `the criteria listed in section 18-3302(11), Idaho Code, or does not meet all of the foll…`

## Samples — us_il_regulations

Truncated heads (each begins mid-word):

- `STATE_IL_IAC_T14_P130_S130_APPENDIX` — `has
become effective in the form found acceptable.
The cash proceeds covered by this
A…`
- `STATE_IL_IAC_T14_P130_S130_APPENDIX` — `n designated by law, and the successors in
such office, attorney for the applicant in s…`
- `STATE_IL_IAC_T23_P33_S33_Appendix` — `s, and
community partnerships and includes a focus on the future.
Standard Element 1.2
…`
- `STATE_IL_IAC_T23_P75_S75_430` — `site (www.ilaged.org) and support content for the State
Board of Education's agricultur…`
- `STATE_IL_IAC_T23_P75_S75_500` — `th and/or
career success.  Examples of these activities include leadership training or…`
- `STATE_IL_IAC_T23_P75_S75_640` — `as a
condition for their continued receipt of assistance during the internship
program…`
- `STATE_IL_IAC_T23_P_S100_TABLE` — `ersonnel
who are not on the district's payroll, and other services the district may
pu…`
- `STATE_IL_IAC_T23_P_S2050_APPENDIX` — `ff regularly conducts
a developmental screening with an appropriate standardized tool f…`

## Samples — us_in_court_rules

Truncated heads (each begins mid-word):

- `SRULES_IN_INTERP_R2` — `a) This policy applies to interpreters who are certified in foreign language interpretat…`
- `SRULES_IN_INTERP_R4` — `a) Any person may initiate a complaint within 180 days of the egregious act by filing it…`
- `SRULES_IN_INTERP_R5` — `a) If probable cause is found, the Chief Administrative Officer (CAO) of the Indiana Off…`
- `SRULES_IN_INTERP_R6` — `a) All disciplinary sanctions imposed shall become public unless dismissed, resolved inf…`

## Samples — us_ks_guidance

Truncated heads (each begins mid-word):

- `KS_INS_B_1995_21` — `file in
R. K. K.

Kathleen Sebelius

Commissioner of Insurance

Kansas Insurance Departm…`

## Samples — us_ky_regulations

Truncated heads (each begins mid-word):

- `STATE_KY_KAR_T012_C003_R012` — `ent as established in 12 KAR 3:027; (6) A statement of nutritional adequacy or purpose i…`
- `STATE_KY_KAR_T012_C003_R039` — `te and balanced," "perfect," "scientific," or "100% nutritious" if the product and claim…`
- `STATE_KY_KAR_T103_C005_R180` — `estate, trust partnership, limited liability company, association, organization, joint v…`
- `STATE_KY_KAR_T103_C005_R190` — `rtment" means the Kentucky Department of Revenue. (8) "Person" means any individual, cor…`
- `STATE_KY_KAR_T103_C044_R120` — `st indicating the reason for the request to the Department of Revenue with the following…`
- `STATE_KY_KAR_T105_C001_R150` — `of any down payment to be made by the employee, whether by personal check or rollover or…`
- `STATE_KY_KAR_T105_C001_R300` — `eive the number of months of service credit determined by dividing the actual number of …`
- `STATE_KY_KAR_T201_C002_R250` — `nt shall not make copies or reports of records that do not regard the issue of the licen…`

## Samples — us_la_constitutions

Truncated heads (each begins mid-word):

- `SCONST_LA_AIII_S12` — `ing fines, penalties, and forfeitures; refunding moneys legally paid into the treasury. …`

## Samples — us_la_court_rules

Truncated heads (each begins mid-word):

- `SRULES_LA_DCR_TII_R9_4` — `memoranda be filed with the clerk of court or sent directly to the presiding judge. 

(g…`
- `SRULES_LA_DCR_TII_R9_5` — `for Judgment 

(a) All judgments, orders, and rulings requiring the court=s signature sh…`
- `SRULES_LA_DCR_TIV_R24_6` — `a Self-Represented Party Has Filed an Answer 

Courts that have adopted court-specific r…`
- `SRULES_LA_DCR_TIV_R34_2` — `for Filing 

All objections to hearing officer recommendations and judgments of domestic…`
- `SRULES_LA_DCR_TV_R44_1` — `to the court regarding recommendations for disposition, including any required supervisi…`
- `SRULES_LA_DCR_TV_R45_2` — `to the court regarding recommendations for disposition and reports pertaining to review …`
- `SRULES_LA_ROPC_R1_11` — `and Employees 
(a) 
Except as law may otherwise expressly permit, a lawyer who has forme…`
- `SRULES_LA_URCA_R1_1_2` — `to the Rules of Court shall be promulgated and published in the same 
manner, and shall …`

## Samples — us_la_statutes

Truncated heads (each begins mid-word):

- `STATE_LA_Crevised-statutes_T10_S12-106` — `referred to in Paragraph (d)(1) of this Section, that the transferee has the power to:

…`
- `STATE_LA_Crevised-statutes_T10_S7-106` — `e person of an interest in the document:

(1) has control of the document and acknowledg…`
- `STATE_LA_Crevised-statutes_T10_S7-210` — `e, if any, for delivery on demand to any person to which the warehouse would have been b…`
- `STATE_LA_Crevised-statutes_T10_S8-108` — `the security certificate warrants only that the delivering person has authority to act f…`
- `STATE_LA_Crevised-statutes_T10_S9-334` — `ted to the security interest or disclaimed an interest in the goods as fixtures; or

(2)…`
- `STATE_LA_Crevised-statutes_T10_S9-615` — `or a secondary obligor if:

(1) the transferee in the disposition is the secured party, …`
- `STATE_LA_Crevised-statutes_T11_S142` — `putation.

(2) If the benefit computation of any system requires the use of a minimum nu…`
- `STATE_LA_Crevised-statutes_T11_S1481` — `itor the amount of the shortfall and its cause. In the event the shortfall is due to the…`

## Samples — us_md_guidance

Truncated heads (each begins mid-word):

- `MD_INS_B_01-11` — `www.mdinsurance.state.md.us
Outside Baltimore Metro Area, Toll Free 1-800-492-6116
TTY U…`
- `MD_INS_B_01-12` — `www.mdinsurance.state.md.us
Outside Baltimore Metro Area, Toll Free 1-800-492-6116
TTY U…`
- `MD_INS_B_13-28` — `signatuare on original

February 2014 
SUMMARY OF REVISIONS – February 2014 edition 
 
 …`
- `MD_INS_B_16-30` — `civil action proceeds through each level of adjudication and as each adjudicatory body 
…`
- `MD_INS_B_19-10` — `at b..tlQs://www.insurancecompact.org/l[l/eekly tips/compact applications for child life…`

## Samples — us_md_regulations

Truncated heads (each begins mid-word):

- `STATE_MD_COMAR_10_07_01_01` — `p or organization.
(6) “Appointment” means designation of a physician to have staff priv…`
- `STATE_MD_COMAR_10_09_02_07` — `ordance with §D of this regulation .
F. The Program shall reimburse providers up to the …`
- `STATE_MD_COMAR_10_09_29_01` — `he administrative unit of the Department of Human Services and its affiliated local depa…`
- `STATE_MD_COMAR_10_09_36_01` — `ervice; or
(c) All services for one participant within a bill.
(5) Clean Claim.
(a) “Cle…`
- `STATE_MD_COMAR_10_09_36_06` — `e service.
(b) The Program shall only pay claims for services provided on different date…`
- `STATE_MD_COMAR_10_09_45_03` — `evels of care listed in §D(2) or (3) of this regulation.
(2) Level I—General. For a maxi…`
- `STATE_MD_COMAR_10_09_59_01` — `ing stated in COMAR 10.09.50.01 .
(8) “Local school system (LSS)” means a local public s…`
- `STATE_MD_COMAR_10_09_90_11` — `e participant’s needs and progress shall be facilitated by the care coordinator and moni…`

## Samples — us_me_court_rules

Truncated heads (each begins mid-word):

- `SRULES_ME_JUDCOND_R1_2` — `language expands the second phrase of 1993 Canon 2(A), which directed that a 
judge “sha…`
- `SRULES_ME_JUDCOND_R1_3` — `worded. The 1993 Canon 2(B) states: 

B. Preventing Improper Influence. A judge shall no…`
- `SRULES_ME_JUDCOND_R2_1` — `worded but has the same effect as 1993 Canon 3(A). The 1993 Advisory 
Committee’s Note t…`
- `SRULES_ME_JUDCOND_R2_10` — `fulfilling the judge’s judicial or administrative responsibilities, when the 
statement …`
- `SRULES_ME_JUDCOND_R2_12` — `performance of their other judicial responsibilities” that appears in 1993 Canon 
3(C)(3…`
- `SRULES_ME_JUDCOND_R2_13` — `particularly addressing (1) appointment of persons who have made 
contributions in Proba…`
- `SRULES_ME_JUDCOND_R2_14` — `arises only when a judge has “actual knowledge” that a lawyer’s or a judge’s 
performanc…`
- `SRULES_ME_JUDCOND_R2_15` — `uses of the terms “shall” and “should,” depending on the clarity of the 
information ind…`

## Samples — us_me_regulations

Truncated heads (each begins mid-word):

- `STATE_ME_CMR_00_031_270` — `section.
(A)	"Accident," "Accidental Injury," or "Accidental Means" shall be defined to …`
- `STATE_ME_CMR_00_137_21` — `purpose.
		All new agents must complete training as required in the agent agreement form…`
- `STATE_ME_CMR_00_137_28` — `i.	To be qualified to lead trips on inland waters, the applicant shall have successfully…`
- `STATE_ME_CMR_00_144_1` — `authority.
Appellant - Any person, institution, business organization, or other entity r…`
- `STATE_ME_CMR_00_144_109` — `section.1.03-1	Structure and ProcessThe QMP structure and process must include the f…`
- `STATE_ME_CMR_00_144_115` — `section.
	20.3.8	When a facility is purchased from a seller who has been terminated from…`
- `STATE_ME_CMR_00_144_119` — `authority. All complaint investigations will be unannounced.  3.B.4.	Upon receipt of a…`
- `STATE_ME_CMR_00_144_232` — `purpose.SECTION 408.0 WELL INFORMATION408.1 Required well information recording: Up…`

## Samples — us_me_statutes

Truncated heads (each begins mid-word):

- `STATE_ME_T22_S2_C258-A_S1471-V` — `l. Representation. When the board, under section 1471‑M , considers the designation of a…`
- `STATE_ME_T22_S3_C857_S3293` — `l. Disclosure to state employees. Confidential information that is relevant to a grievan…`

## Samples — us_mi_court_rules

Truncated heads (each begins mid-word):

- `SRULES_MI_AO_R1985_5` — `the Care of Children
[Entered April 30, 1985.]
On order of the Court, the Juvenile Court…`
- `SRULES_MI_AO_R1988_3` — `for the Care of Children
[Entered April 29, 1988. See AO No. 1985-5.]…`
- `SRULES_MI_AO_R1990_3` — `in the Courts and the Task Force on Racial/Ethnic Issues in the Courts 
[Entered June 12…`
- `SRULES_MI_AO_R1994_2` — `the Filing and Transmission of Court Documents
[Entered February 3, 1994; rescinded by o…`
- `SRULES_MI_AO_R2002_3` — `and Probate Court)
[Entered May 2, 2002; effective September 1, 2002.]
On order of the C…`
- `SRULES_MI_AO_R2004_2` — `for Barry, Berrien, Isabella, Lake, and Washtenaw Counties, and for the 46th 
Circuit Co…`
- `SRULES_MI_AO_R2005_1` — `the 41st Circuit Court, the 95B District Court, and the Iron County Probate 
Court
[Ente…`
- `SRULES_MI_AO_R2006_7` — `of Circuit Court and Probate Court)
[Entered September 19, 2006; rescinded by order ente…`

## Samples — us_mi_statutes

Truncated heads (each begins mid-word):

- `STATE_MI_C125_AAct-376-of-1996_S125.2688d` — `existing recovery zone to add additional property under the same terms and conditions as…`
- `STATE_MI_C125_AAct-381-of-1996_S125.2663` — `erty, and a statement of whether personal property is included as part of the eligible p…`
- `STATE_MI_C125_AAct-381-of-1996_S125.2665` — `the department denies all or a portion of a work plan under this subdivision, the author…`
- `STATE_MI_C141_AAct-243-of-1980_S141.932` — `s of outstanding loans; with any provision of this act; or, in relation to a loan under …`
- `STATE_MI_C205_AAct-122-of-1941_S205.27a` — `nd establishes that the assessment of the purchaser or succeeding purchaser would permit…`
- `STATE_MI_C205_AAct-122-of-1941_S205.30c` — `that person providing the following relief:

(a) Notwithstanding section 28(1)(e) of thi…`
- `STATE_MI_C205_AAct-167-of-1933_S205.53` — `ed by the state treasurer or his or her designee is guilty of a misdemeanor punishable b…`
- `STATE_MI_C205_AAct-167-of-1933_S205.75` — `health initiative fund created in section 5911 of the public health code, 1978 PA 368, M…`

## Samples — us_mn_guidance

Truncated heads (each begins mid-word):

- `MN_INS_GUID_2018_HEALTH_CARRIER_LETTER` — `ffll MINNeSOTA 
Date: May 3, 2017 
To: All Minnesota Health Plan Companies 
This letter …`
- `MN_INS_GUID_2019_HEALTH_CARRIER_LETTER_SUPPLEMENT` — `ffl1 MINNeSOTA 
Date: May 8, 2018 
To: 
All Minnesota Health Plan Companies 
Re: 
Supple…`

## Samples — us_mn_regulations

Truncated heads (each begins mid-word):

- `STATE_MN_ADR_4410_0200` — `n 13. Subp. 54. Negative declaration. "Negative declaration" means a written statement b…`
- `STATE_MN_ADR_4410_1100` — `ceipt of the petition with a written explanation of why it fails to comply. Subp. 6. EAW…`
- `STATE_MN_ADR_6232_0300` — `under Minnesota Statutes, section 97B.055 , subdivision 3, who are hunting in a lottery …`
- `STATE_MN_ADR_6237_0200` — `as a group. Group applications shall either be all selected or none selected. Applicatio…`
- `STATE_MN_ADR_9210_0100` — `of energy to markets. Subp. 11. Preliminary design and engineering/architectural plans. …`
- `STATE_MN_ADR_9210_0180` — `and operational according to the terms and conditions of the grant agreement, including …`

## Samples — us_mo_guidance

Truncated heads (each begins mid-word):

- `MO_INS_WCTAX_2019` — `nnne ini nr
3315 WestTruman Boulevard. Room 131
MICn&LLLPFJSO
uiviiun ui
P.O.BoxSS
GOVEP…`

## Samples — us_mo_statutes

Truncated heads (each begins mid-word):

- `STATE_MO_C143_S143.801` — `not filed within the ninety-day period therein specified, interest on any resulting refu…`

## Samples — us_ms_court_rules

Truncated heads (each begins mid-word):

- `SRULES_MS_MCLE_R1` — `a. There is hereby established a Commission on Continuing Legal Education
(hereinafter r…`
- `SRULES_MS_MCLE_R3` — `a. Each attorney licensed to practice law in the State of Mississippi shall attend, or
c…`
- `SRULES_MS_MCLE_R6` — `a.
As soon as practicable after August 15 of each year, the Commission shall
compile the…`
- `SRULES_MS_MCLR_R10` — `signs a collaborative law participation agreement, a prospective collaborative lawyer 
s…`
- `SRULES_MS_MCLR_R11` — `the dynamics of domestic violence and take into consideration, in assessing whether to 
…`
- `SRULES_MS_MCLR_R12` — `communication is confidential to the extent agreed by the parties in a signed record or …`
- `SRULES_MS_MCLR_R18` — `or circumstance is held invalid, the invalidity does not affect other provisions or 
app…`
- `SRULES_MS_MCLR_R5` — `emergency orders to protect the health, safety, welfare, or interest of a party or other…`

## Samples — us_nc_court_rules

Truncated heads (each begins mid-word):

- `SRULES_NC_NCARB_R6` — `similar form if this form is modified and/or 
replaced by the Administrative Office of t…`

## Samples — us_nd_court_rules

Truncated heads (each begins mid-word):

- `SRULES_ND_LOCAL_east_central_R1_V19980101_20030101` — `a) Hearings on Motions.
Parties initiating motions shall file with the Clerk of Court a …`
- `SRULES_ND_NDRPROFCONDUCT_R8_3_V20040801_20060801` — `violation of these rules that raises a substantial question as to that lawyer's honesty,…`

## Samples — us_nh_court_rules

Truncated heads (each begins mid-word):

- `SRULES_NH_CIRPROB_RULES_30_32_RESERVED_FOR_FUTURE_USE_R35` — `a. Discovery Methods. Parties may obtain discovery by one or more of the following metho…`
- `SRULES_NH_CIRPROB_RULES_30_32_RESERVED_FOR_FUTURE_USE_R78_A` — `a) Request that Proceedings be Recorded. A Party may request that any probate proceeding…`
- `SRULES_NH_SUPER_R307` — `a. Within 10 days after the date identified for disclosure of defendant’s experts, all p…`
- `SRULES_NH_SUPER_R309` — `a. Special procedural requests
b. Pre-hearing motions
c. Final witness list, expert and …`
- `SRULES_NH_SUPER_R310` — `a. A brief summary statement by each party
b. Medical records
c. Expert opinions submitt…`
- `SRULES_NH_SUPER_R311` — `a. In advance of the panel hearing, counsel and self-represented parties, if any, shall …`
- `SRULES_NH_SUPER_R312` — `a. Offers of Proof – Except by agreement of the parties, offers of proof, including expe…`

## Samples — us_nh_guidance

Truncated heads (each begins mid-word):

- `NH_INS_B_2015-003-AB` — `d...:.*;..,, 
. 
. 
I 
+ 
+ 
,I, tit•• 
~
,,• 
•,.I 
The State of New Hampshire
Insuranc…`
- `NH_INS_B_2020-023-AB` — `a 
' 
{"!l!liiiilF'I 
The State of New Hampshire
Insurance Department 
21 South Fruit St…`
- `NH_INS_B_2021-001-AB` — `f. 
• •• ·~ 
Jf. 
+ 
.,. 
~ 
J 
~ 
.. 
The State of New Hampshire 
Insurance Department …`

## Samples — us_nj_constitutions

Truncated heads (each begins mid-word):

- `SCONST_NJ_AI_S2` — `a. All political power is inherent in the people. Government is instituted for the prote…`
- `SCONST_NJ_AV.I_S10` — `a. The Governor and the Lieutenant Governor shall each receive for services a salary, wh…`
- `SCONST_NJ_AVI.VIII_S1` — `a. On or before July 1, 1997: (1) The State shall be required to pay for certain judicia…`
- `SCONST_NJ_AVIII.II_S3` — `a. The Legislature shall not, in any manner, create in any fiscal year a debt or debts, …`
- `SCONST_NJ_AVIII.I_S3` — `a. Any citizen and resident of this State now or hereafter honorably discharged or relea…`
- `SCONST_NJ_AVIII.I_S7` — `a. No tax shall be levied on personal incomes of individuals, estates and trusts of this…`

## Samples — us_nj_statutes

Truncated heads (each begins mid-word):

- `STATE_NJ_T10_C4_S4-15` — `a. Any action taken by a public body at a meeting which does not conform with the provis…`
- `STATE_NJ_T10_C4_S4-9` — `a. Except as provided by subsection b. of this section, or for any meeting limited only …`
- `STATE_NJ_T10_C5_S5-35` — `a. Any public works contract including any subcontract awarded thereunder to any contrac…`
- `STATE_NJ_T12A_C3_S3-102` — `a. This chapter applies to negotiable instruments. It does not apply to money, to paymen…`
- `STATE_NJ_T12A_C3_S3-103` — `a. As used in this chapter: (1) "Acceptor" means a drawee who has accepted a draft. (2) …`
- `STATE_NJ_T12A_C3_S3-104` — `a. Except as provided in subsections c. and d. of this section, "negotiable instrument" …`
- `STATE_NJ_T12A_C3_S3-105` — `a. "Issue" means the first delivery of an instrument by the maker or drawer, whether to …`
- `STATE_NJ_T12A_C3_S3-106` — `a. Except as provided in this section, for the purposes of subsection a. of 12A:3-104, a…`

## Samples — us_nm_regulations

Truncated heads (each begins mid-word):

- `SREGS_NM_T1_C11_P2_S2` — `all county clerks who accept and record real property records electronically.…`
- `SREGS_NM_T1_C13_P3_S2` — `all state agencies…`
- `SREGS_NM_T1_C13_P4_S2` — `all state agencies as defined by the Public Records Act, Section 14-3-1 et seq. NMSA 197…`
- `SREGS_NM_T3_C5_P4_S8` — `taxpayer's income from business activity is taxable without this state if such taxpayer,…`
- `SREGS_NM_T5_C7_P18_S11` — `programs established under the auspices of the western interstate commission on higher e…`
- `SREGS_NM_T7_C4_P6_S7` — `as used in these regulations: A. “Blood borne pathogens” means the hepatitis B virus (HB…`
- `SREGS_NM_T8_C370_P16_S16` — `a license will automatically expire at midnight on the day indicated on the license as t…`

## Samples — us_nv_court_rules

Truncated heads (each begins mid-word):

- `SRULES_NV_CIVIL_TRAFFIC_INFRACTIONS_R4_2` — `q1w2e3NRCTI Form A—Civil Infraction Response NRCTI Form A—Civil Infraction Response NAME…`

## Samples — us_nv_guidance

Truncated heads (each begins mid-word):

- `NV_INS_B_95_003` — `it()B lllLl-LR
()ouernot
,iTAIE T)F I.IEVADA
DEPARTMENT OF BUSINESS AND INDUSTRY
DTVISIO…`

## Samples — us_ny_court_rules

Truncated heads (each begins mid-word):

- `SRULES_NY_22NYCRR_P17_S17_1` — `a) Judicial visits to facilities listed below inform judges about the conditions in the …`
- `SRULES_NY_22NYCRR_P521_S521_2` — `required.
An applicant under this Part
shall file with the clerk of the Appellate Divisi…`
- `SRULES_NY_22NYCRR_P521_S521_3` — `of practice.
A person licensed to
practice as a legal consultant under this Part may ren…`
- `SRULES_NY_22NYCRR_P521_S521_4` — `and obligations.
Subject to the limitations set forth in section 521.3 of this Part, a p…`

## Samples — us_oh_court_rules

Truncated heads (each begins mid-word):

- `SRULES_OH_CAPITAL_R3_01` — `division (A) of this rule. The attorney shall submit a new application demonstrating tha…`
- `SRULES_OH_JCOND_R2_1` — `extrajudicial,” thus retaining language found in the Ohio Code. “Other” is broader and m…`
- `SRULES_OH_JCOND_R2_15` — `reporting requirement once a judge has knowledge of a violation by a lawyer or judge. Ru…`
- `SRULES_OH_JCOND_R2_5` — `compliance with the Ohio Rules of Superintendence. Among other requirements, the Rules o…`
- `SRULES_OH_JCOND_R2_9` — `the necessity to make provision for the manner in which communications with parties and …`
- `SRULES_OH_JCOND_R3_1` — `the “incidental use” exception to any extrajudicial activity. The Model Code limits the …`
- `SRULES_OH_JCOND_R3_11` — `with a business entity and to add a general exemption for writing and teaching activitie…`
- `SRULES_OH_JCOND_R3_12` — `commensurate” found in the comments to Model Rule 3.12. Comment [1] is modified remove t…`

## Samples — us_oh_regulations

Truncated heads (each begins mid-word):

- `STATE_OH_ADC_120_1_09` — `villages. April 17, 2026 111.15 County commissioners, public defenders, county public de…`
- `STATE_OH_ADC_120_1_15` — `and public defender salaries. April 17, 2026 111.15 To qualify for reimbursement, counti…`
- `STATE_OH_ADC_145_1_41` — `determination. January 16, 2026 111.15 (A) In making any determination as to whether an …`
- `STATE_OH_ADC_1501_14_1_12` — `code and map symbols. February 1, 2024 119.03 (A) Submit maps along with permit applicat…`
- `STATE_OH_ADC_1501_9_4_04` — `construct an oil and gas waste facility. January 13, 2022 119.03 (A) This rule applies t…`
- `STATE_OH_ADC_173_9_06` — `paid direct-care positions: disqualifying offenses. February 1, 2026 119.03 (A) No respo…`
- `STATE_OH_ADC_3301_13_06` — `tests. May 12, 2024 119.03 (A) Each participating school will ship all test materials de…`
- `STATE_OH_ADC_3339_3_06` — `discrimination. October 1, 2019 111.15 (A) Harassment and discrimination are prohibited …`

## Samples — us_ok_statutes

Truncated heads (each begins mid-word):

- `STATE_OK_T10A_S10A-1-1-101` — `chapter and part captions.

Oklahoma Statutes - Title 10A. Children and Juvenile Code Pa…`
- `STATE_OK_T10A_S10A-1-2-101v1` — `reporting child abuse or neglect – Hotline requirements – Reporting

abuse or neglect – …`
- `STATE_OK_T10A_S10A-1-2-101v2` — `reporting child abuse or neglect – Hotline requirements – Reporting

abuse or neglect – …`
- `STATE_OK_T10A_S10A-1-2-101v3` — `reporting child abuse or neglect – Hotline requirements – Reporting

abuse or neglect – …`
- `STATE_OK_T10A_S10A-1-2-102v1` — `reports of child abuse.

A. 1. Upon receipt of a report that a child may be abused,

neg…`
- `STATE_OK_T10A_S10A-1-2-102v2` — `referrals by Department of Human Services – Investigations by law

enforcement agencies.…`
- `STATE_OK_T10A_S10A-1-2-105` — `of family – Immediate removal of child - Report – Voluntary services

- Temporary restra…`
- `STATE_OK_T10A_S10A-1-2-108` — `sexual exploitation and neglect.

A. There is hereby established within the Department o…`

## Samples — us_or_court_rules

Truncated heads (each begins mid-word):

- `SRULES_OR_ORAP_R16_10` — `eFILERS
(1) 
Authorized eFilers 

(a) 
Any person may register to become an eFiler. 

(b…`

## Samples — us_or_guidance

Truncated heads (each begins mid-word):

- `OR_INS_B_2001_09` — `regon
Departmentof Consumer
and Business
Services
Insurance
Division
350 Wmter
St. NE, R…`
- `OR_INS_B_2014_03` — `regan 
John A. Kitzhabel~ MD, Governor 
Department of Consumer and Business Services 
In…`
- `OR_INS_B_2017_04` — `reg on 
Kale Brown, Governor 
Department of Consumer and Business Services 
Division of …`
- `OR_INS_B_2017_07` — `reg on 
Kate Brown, Governor 
Department of Consumer and Business Services 
Division of …`
- `OR_INS_B_2018_01` — `reg on 
Kate Brown, Governor 
Department of Consumer and Business Services 
Division of …`
- `OR_INS_B_2018_03` — `r:rnJr DS I Consumer and 
W'-Cl 
Business Services 
350 Winter Street NE, Room 200, P.O.…`

## Samples — us_or_statutes

Truncated heads (each begins mid-word):

- `STATE_OR_T14_C137_S137.690` — `a. Any person who is convicted of a major felony sex crime, who has one (or more) previo…`

## Samples — us_pa_constitutions

Truncated heads (each begins mid-word):

- `SCONST_PA_AIII_S19` — `forces. The General Assembly may make appropriations of money to institutions wherein th…`
- `SCONST_PA_AII_S9` — `of members. The Senate shall, at the beginning and close of each regular session and at …`
- `SCONST_PA_AIV_S18` — `of State Treasurer to become Auditor General. The terms of the Auditor General and of th…`
- `SCONST_PA_AI_S10` — `eminent domain. Except as hereinafter provided no person shall, for any indictable offen…`
- `SCONST_PA_AI_S29` — `ethnicity. Equality of rights under the law shall not be denied or abridged in the Commo…`
- `SCONST_PA_AX_S3` — `corporation laws. All charters of private corporations and all present and future common…`
- `SCONST_PA_AX_S4` — `right of eminent domain. Municipal and other corporations invested with the privilege of…`

## Samples — us_pa_statutes

Truncated heads (each begins mid-word):

- `STATE_PA_T3_C41_S4175` — `weighing or measuring device which is marked as described above, provided, however, that…`
- `STATE_PA_T3_C71_S7110` — `potatoes or agricultural or vegetable seeds or planting material for vegetative propagat…`

## Samples — us_pr_court_rules

Truncated heads (each begins mid-word):

- `SRULES_PR_RAAO_R16` — `abogado o una abogada de oficio 
Cuando un abogado o una abogada de oficio opte por adel…`
- `SRULES_PR_RAAO_R18` — `oficio; compensación, pago por sus servicios y rembolso de gastos de litigación 
De esta…`
- `SRULES_PR_RAAO_R3` — `asignación de oficio del tribunal 
Quien ejerce la abogacía tiene la responsabilidad éti…`
- `SRULES_PR_RAAO_R8` — `y notificación de la orden de asignación; deberes del tribunal 
(a)
Cuándo procede la de…`
- `SRULES_PR_RAAO_R9` — `y notificación de la orden de asignación; deberes del abogado o de la abogada 
(a) 
Resp…`
- `SRULES_PR_RADM_R10_1_1` — `reválida tendrá derecho a: 
(a)
examinar sus contestaciones a las preguntas de discusión…`
- `SRULES_PR_RADM_R10_2_1` — `arancel en sellos de Rentas Internas: veinte dólares ($20) por las contestaciones al 
ex…`
- `SRULES_PR_RADM_R10_3_1` — `ejercer sus derechos según la Regla 10.1.1 de este Reglamento, deberá hacer dicha 
solic…`

## Samples — us_pr_guidance

Truncated heads (each begins mid-word):

- `PR_INS_B_CN-EC-I-3-4291` — `u:r400 
LlllI£ 
4S0C14DO Dl PUERTO alCO
OFICINA 
DEL 
COMISIONADO 
DE SECUROS
Carta 
Nor…`

## Samples — us_pr_statutes

Truncated heads (each begins mid-word):

- `STATE_PR_INCENTIVOS_SEC2073_09` — `a) En proyectos de Viviendas de Interés Social aprobado y subsidiado total o parcialment…`
- `STATE_PR_INCENTIVOS_SEC6060_03` — `a) La derogación de cualquier ley, artículo o disposición mediante este Código no afecta…`
- `STATE_PR_LEY_0003_1936_ART3` — `ons 48-&, 61-a, 61-&, 61-c, 61-d, 61-e, 62-a, 62-6, 70-a, que se designarán secciones 48…`
- `STATE_PR_LEY_0003_1936_ART4` — `lared unconstitutional by a court of competent jurisdic- con jurisdicción competente, di…`
- `STATE_PR_LEY_0003_1936_ART6` — `h part thereof as may be necessary, is hereby appro- cientos cincuenta mil (250,000) dól…`
- `STATE_PR_LEY_0115_1966_ART2` — `del S. 448) de su aprobación. [NÚM. 116] Aprobada en 2k de junio de 1966. [Aprobada en 2…`
- `STATE_PR_LEY_101_2020_ART3` — `es públicas e instrumentalidades. La Política de Administración de Deuda deberá (a) impo…`
- `STATE_PR_LEY_102_1969_ART15` — `de julio de 1969. Nota. Este documento fue compilado por personal de la Oficina de Geren…`

## Samples — us_ri_court_rules

Truncated heads (each begins mid-word):

- `SRULES_RI_EVID_R1001` — `are applicable: 
(1) Writings and Recordings. “Writings” and “recordings” consist of let…`
- `SRULES_RI_EVID_R1002` — `recording, or photograph, the original writing, recording, or photograph is required, 
e…`
- `SRULES_RI_EVID_R1003` — `extent as an original unless (1) a genuine question is raised as to the authenticity of …`
- `SRULES_RI_EVID_R1004` — `and other evidence of the contents of a writing, recording, or photograph is 
admissible…`
- `SRULES_RI_EVID_R1005` — `document authorized to be recorded or filed and actually recorded or filed, including 
d…`
- `SRULES_RI_EVID_R1006` — `photographs which cannot conveniently be examined in court may be presented in 
the form…`
- `SRULES_RI_EVID_R1007` — `recordings, or photographs may be proved by the testimony or deposition of the party 
ag…`
- `SRULES_RI_EVID_R1008` — `evidence of contents of writings, recordings, or photographs under these rules 
depends …`

## Samples — us_ri_statutes

Truncated heads (each begins mid-word):

- `STATE_RI_T19_C19-34_S19-34-3` — `lf a regulated institution submits a report of suspected financial exploitation or abuse…`

## Samples — us_sc_constitutions

Truncated heads (each begins mid-word):

- `SCONST_SC_AIV_S21` — `esidue thereof, it shall become a law as to the residue in like manner as if he had sign…`
- `SCONST_SC_AVIII_S13` — `her in-lieu-of payments that would have been due and payable except for the exemption he…`
- `SCONST_SC_AX_S15` — `t, the State Treasurer shall withhold from such school district sufficient moneys from a…`

## Samples — us_sc_guidance

Truncated heads (each begins mid-word):

- `SC_INS_B_2007-05` — `of Insurance 
Capitol Center 
1201 Main Street, Suite 1000 
Columbia, South Carolina 292…`
- `SC_INS_B_2009-08` — `su 
South Carolina 
Department of Insurance 
C:t(litol ('enter 
1201 \lain Street. Suite…`

## Samples — us_sc_regulations

Truncated heads (each begins mid-word):

- `STATE_SC_CODEREGS_117_1840_2` — `a. Section 12-4-560 of the South Carolina Code of Laws provides, in part, that the Depar…`
- `STATE_SC_CODEREGS_17_21` — `a. A mobile barbershop must be a self-contained unit sufficiently equipped to provide ba…`
- `STATE_SC_CODEREGS_17_22` — `a. A portable barber operation is a licensed registered barber or master hair care speci…`
- `STATE_SC_CODEREGS_5_610` — `a. Class I Price of fluid milk means the Uniform Milk price in South Carolina published …`
- `STATE_SC_CODEREGS_5_611` — `a. The average production price shall be posted on the Department’s website and will be …`
- `STATE_SC_CODEREGS_65_30` — `a. To deny an employee a reasonable accommodation when a medical need arises from pregna…`
- `STATE_SC_CODEREGS_83_1` — `a. The definitions and meanings of terms shall be as follows:

    b. These regulations …`
- `STATE_SC_CODEREGS_91_31` — `a. Names, addresses and authorized statistical data of licensed nurses may be released u…`

## Samples — us_sd_regulations

Truncated heads (each begins mid-word):

- `STATE_SD_ARSD_T20_A86_C02_S14` — `n a proceeding seeking an order of inactive status, probation, or suspension based upon …`

## Samples — us_sd_statutes

Truncated heads (each begins mid-word):

- `STATE_SD_T10_C46_S10-46-1` — `yright.

(9) "Purchase," any transfer, exchange, or barter, conditional or otherwise, in…`

## Samples — us_tn_court_rules

Truncated heads (each begins mid-word):

- `SRULES_TN_TRAP_R20A` — `a) Definitions.
(1) "Facsimile filing" means the facsimile transmission of an original d…`

## Samples — us_tn_guidance

Truncated heads (each begins mid-word):

- `TN_INS_B_19880901_9_1_88` — `c 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURANCE 
500 JAMES ROBERTSON PARKWAY…`
- `TN_INS_B_19890327_3_27_89` — `fM;;&-e[ -
Jie_, 1/j;;/!9 tu!W/j 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURAN…`
- `TN_INS_B_19900328_3_28_90` — `r"'\ 
., 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURANCE 
LEGAL SERVICES 
NED …`
- `TN_INS_B_19920211_3_21_92` — `r.... 
' 
.i 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURANCE 
500 JAMES ROBERT…`
- `TN_INS_B_19930421_4_21_93` — `lr"'\ 
\ 
NED McWHERTER 
GOVERNOR 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURA…`
- `TN_INS_B_19940706_7_6_94` — `il.: . 
.....,.... 
~ 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURANCE 
500 JAM…`
- `TN_INS_B_20150213_021315_Rebating_Bulletin` — `i 
I 
~ 
-~ 
I ' I 
I 
BILL HASLAM 
GOVERNOR 
TO: 
FROM: 
RE: 
DATE: 
STATE OF TENNESSEE…`
- `TN_INS_B_20230511_UnintendedTaxConsequencesBulletin0511202` — `tn.gov/commerce 
STATE OF TENNESSEE 
DEPARTMENT OF COMMERCE AND INSURANCE 
500 JAMES ROB…`

## Samples — us_tn_statutes

Truncated heads (each begins mid-word):

- `STATE_TN_T11_C25_S11-25-107` — `daries of the authority; (15) Provide recreational facilities; (16) Lease authority-owne…`
- `STATE_TN_T12_C10_S12-10-109` — `comptroller of the treasury or the comptroller's designee to review loan agreements ente…`
- `STATE_TN_T13_C20_S13-20-104` — `newal projects for such municipality with respect to one (1) or more redevelopment or ur…`
- `STATE_TN_T29_C39_S29-39-104` — `icable to discovery, nor does it apply to the management of records in the normal course…`
- `STATE_TN_T56_C6_S56-6-1205` — `lf an owner or its employee or authorized representative violates this part, the commiss…`
- `STATE_TN_T8_C13_S8-13-108` — `ch the register shall register, separately from land titles, in the order in which they …`
- `STATE_TN_T8_C34_S8-34-302` — `ition; however, the speaker need not appoint any person so recommended; and (16) One (1)…`
- `STATE_TN_T9_C21_S9-21-306` — `disposition thereof; (10) Redeem the revenue bonds, and covenant for their redemption an…`

## Samples — us_tx_guidance

Truncated heads (each begins mid-word):

- `TX_INS_B_0064_96` — `ctions to be taken are spelled out as follows:

a. for renewal offers made for policies …`

## Samples — us_ut_court_rules

Truncated heads (each begins mid-word):

- `SRULES_UT_URE_R404` — `a) Character evidence.
(1) Prohibited uses.
Evidence of a person’s character or characte…`

## Samples — us_va_court_rules

Truncated heads (each begins mid-word):

- `SRULES_VA_P1_R1_1B` — `in Circuit Court. 

(a) Jurisdiction After Notice of Appeal. — When a final judgment und…`
- `SRULES_VA_P2_R2_504` — `derived from Code § 8.01-398; and Rule 2:504(b) derived from Code § 19.2-271.2). 

(a) P…`
- `SRULES_VA_P2_R2_609` — `from Code § 19.2-269) 

Evidence that a witness has been convicted of a crime may be adm…`
- `SRULES_VA_P2_R2_706` — `from Code § 8.01-401.1). 

(a) Civil cases. To the extent called to the attention of an …`
- `SRULES_VA_P2_R2_902` — `and Code § 8.01-391(D)). 

Additional proof of authenticity as a condition precedent to …`
- `SRULES_VA_P5A_R5A_13` — `it was mailed, or one day from the date on which the petition was faxed, emailed, or sen…`
- `SRULES_VA_P5_R5_8A` — `promulgated by Order dated Friday, April 30, 2010; effective July 1, 2010. The Rule 
con…`

## Samples — us_va_guidance

Truncated heads (each begins mid-word):

- `VA_INS_AL_1993-06` — `a
STEVEN T. FO STER 
C O M M ISSIO N E R O F IN SU RAN CE
BOX 1157
R IC H M O N D , V IR…`

## Samples — us_va_regulations

Truncated heads (each begins mid-word):

- `STATE_VA_ADC_12_30_40_140` — `a. AFDC-related individuals (except for poverty level related pregnant women, infants, a…`
- `STATE_VA_ADC_12_30_40_160` — `a. Resource standards are based on family size.
b. A single standard is employed in dete…`
- `STATE_VA_ADC_12_30_40_190` — `a. Categorically Needy, Qualified Medicare Beneficiaries, Qualified Disabled and Working…`
- `STATE_VA_ADC_12_30_40_200` — `a. Groups Other Than Qualified Medicare Beneficiaries.
(1) For the prospective period. C…`
- `STATE_VA_ADC_12_30_40_340` — `a. Income and Resource eligibility policies used to determine eligibility for institutio…`

## Samples — us_wa_guidance

Truncated heads (each begins mid-word):

- `WA_OIC_EO_26_02` — `r nr:r nr T1ir r:onr i.r.ii~rR 
'1! ,TE OF WJ',SHINGTON 
flLCO 
DATE: August 07, 2026 
T…`

## Samples — us_wa_regulations

Truncated heads (each begins mid-word):

- `STATE_WA_ADC_131_276_990` — `appendix "a"
request for public record to
state board for community and technical colleg…`
- `STATE_WA_ADC_132K_995_990` — `policies & procedures manual 1111.00 board of trustees 1112.00 Community College Act of …`
- `STATE_WA_ADC_16_139_020` — `level degree of risk to health penalty 1st Violation in a 3-year period a. potential $20…`
- `STATE_WA_ADC_16_139_030` — `level potential for food adulteration penalty 1st Violation in a 3-year period a. potent…`
- `STATE_WA_ADC_16_139_040` — `level degree of knowledge of violation penalty 1st Violation in a 3-year period a. unkno…`
- `STATE_WA_ADC_173_160_990` — `not to scale Figure 1. sealing of unconsolidated formations
not to scale
Figure 1. seali…`
- `STATE_WA_ADC_173_240_095` — `declaration of construction of water pollution
control facilities
Instructions:
A. Upon …`
- `STATE_WA_ADC_173_245_075` — `declaration of construction of water pollution
control facilities
Instructions:
A. Upon …`

## Samples — us_wi_court_rules

Truncated heads (each begins mid-word):

- `SRULES_WI_SCR20B_R20_8_5` — `differs from the ABA Model Rule 8.5. Due to substantive and numbering
differences, speci…`
- `SRULES_WI_SCR60_R60_05` — `should not be read as proscribing participation in de minimis fund-raising
activities so…`

## Samples — us_wi_regulations

Truncated heads (each begins mid-word):

- `STATE_WI_ADC_EL_20_05` — `commission meetings.
(1) The commission shall review the analysis and recommendations of…`

## Samples — us_wi_statutes

Truncated heads (each begins mid-word):

- `STATE_WI_C121_S121.905` — `a. Calculate the sum under subd. 1. for each of the school districts from which territor…`
- `STATE_WI_C13_S13.489` — `b. The report recommending approval of the project is accompanied by a financing proposa…`
- `STATE_WI_C15_S15.197` — `b. At least 6 members shall be physically disabled persons. Two members may be parents, …`
- `STATE_WI_C196_S196.199` — `b. If the alleged failure to comply is not resolved to the satisfaction of the commissio…`
- `STATE_WI_C224_S224.725` — `b. The division may disclose the social security number to the department of children an…`
- `STATE_WI_C343_S343.165` — `d. A valid photo identification card issued by Wisconsin or another jurisdiction, except…`
- `STATE_WI_C49_S49.455` — `b. In any year, $60,000 increased by the same percentage as the percentage increase in t…`
- `STATE_WI_C49_S49.498` — `b. For a violation of sub. (2) (c) 4. , $5,000.

c. For a violation of sub. (13) , $2,00…`

## Samples — us_wv_court_rules

Truncated heads (each begins mid-word):

- `SRULES_WV_RJP_R26` — `a. When competency can be raised.
Competency may be raised, on a good faith basis, durin…`

## Samples — us_wv_statutes

Truncated heads (each begins mid-word):

- `STATE_WV_C15_A1B_S12` — `a. Military property of the state and of the United States shall be issued, safeguarded,…`
- `STATE_WV_C15_A1B_S13` — `a. Members and units of the organized militia shall assemble for drill, or other equival…`
- `STATE_WV_C15_A1B_S4` — `a. Oath, appointment and promotion of officers shall be made in conformity with applicab…`
- `STATE_WV_C15_A1B_S5` — `a. Commissioned officers who shall be rendered surplus by reduction, consolidation, or d…`
- `STATE_WV_C15_A1B_S6` — `a. No officer of the National Guard shall be dismissed unless by reason of resignation, …`
- `STATE_WV_C15_A1B_S9` — `a. Enlisted men may be honorably discharged, discharged, or discharged dishonorably; but…`
- `STATE_WV_C15_A1C_S1` — `a. Any member of the National Guard who has reached the age of sixty-four years, or shal…`
- `STATE_WV_C15_A1D_S12` — `a. Any person who shall, after due warning, trespass upon any armory, camp, range, or ot…`

## Samples — us_wy_constitutions

Truncated heads (each begins mid-word):

- `SCONST_WY_A5_S4` — `f justice from the list within 15 days. (c) There shall be a judicial nominating commiss…`

## Samples — us_wy_statutes

Truncated heads (each begins mid-word):

- `STATE_WY_T27_C14_S27-14-401` — `contracts for bill review, case management and related programs; air ambulance reimburse…`
- `STATE_WY_T34.1_C9_S34.1-9-406` — `on assignment of accounts, chattel paper, payment intangibles and promissory notes ineff…`
- `STATE_WY_T9_C3_S9-3-220` — `participation in the state employees' and officials' group insurance plan; requirements.…`
- `STATE_WY_T9_C3_S9-3-423` — `examinations, tests and evaluations; restoration to service; deduction from benefit for …`

## Why this is a coverage question, not a tidiness question

COV-1A scores a provision `represented` when exactly one dataset row sits at the official
key. That test is **structural**: it asks whether a row exists, never whether the row holds
the whole provision. A truncated body passes it. So the represented rate and the truncation
rate are independent, and a coverage number quoted without the second is an overstatement of
what the corpus can actually answer with.

Text agreement (COV-1A's third dimension) would catch these — but only once the official
oracle is staged and only where the comparison is not `pending`. This audit needs no oracle
at all, so it is available now and stays available for every corpus that has no oracle.

## What the truncation signal is, and is not

The detector is deliberately blunt: the first non-space character of the body is a lowercase
letter. Sampled, it is overwhelmingly genuine mid-word truncation — `'ited States or any
State…'`, `'ublic health, safety, or interest…'`, `'piled by a criminal law enforcement
authority…'`, `'ewed Amendment Number 4…'` — but it is a proxy, not a proof, and a body that
legitimately opens on a lowercase word would be counted. Read the rate with that in view;
the samples below are provided so it can be judged rather than taken on trust.

The converse error is invisible here: a body truncated at a **word boundary** ("United
States or any State…" with an earlier paragraph missing) reads as a clean start and is not
counted. **The measured rate is therefore a lower bound on truncation.**

## Cross-check against CFR-A1

Several `act_id`s counted here as truncated are ones `reports/CFR-A1_commissioning_frame.md`
classified `candidate_segmented` — the stratum whose rows show a mid-thought continuation
seam. That overlap matters for CFR-A2: a "continuation" seam between two rows is equally
consistent with **one row being a truncated capture** as with the two being ordered segments
of one section. It is further evidence for the selection-over-composition respecification —
concatenating a truncated capture to its sibling does not reconstruct the section, it
splices across a hole — and it means the 31 `candidate_segmented` groups need the eCFR
comparison before any of them is treated as composable.


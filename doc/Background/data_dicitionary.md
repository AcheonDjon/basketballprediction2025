To determine the most important features for a team’s win and create weights, we need to identify which factors have the greatest impact on **team_score** relative to **opponent_team_score**. 

### **Feature Importance Analysis**
1. **Scoring Metrics:**
   - **FGM_2, FGM_3, FTM** (Positive impact): These directly contribute to points.
   - **FGA_2, FGA_3, FTA** (Indirect impact): More attempts could lead to higher points, but efficiency (FG% and FT%) matters.
   
2. **Possession and Efficiency Metrics:**
   - **AST (Assists)** (Positive impact): Good ball movement leads to better shots.
   - **BLK (Blocks) & STL (Steals)** (Positive impact): Defensive stops reduce opponent’s chances to score.
   - **TOV & TOV_team** (Negative impact): Losing possession reduces scoring opportunities.

3. **Rebounding Metrics:**
   - **OREB (Offensive Rebounds)** (Positive impact): Leads to second-chance points.
   - **DREB (Defensive Rebounds)** (Positive impact): Prevents opponent second-chance points.

4. **Other Considerations:**
   - **largest_lead** (Positive impact): Teams with large leads usually win.
   - **F_personal & F_tech** (Mixed impact): Too many fouls can give opponents free throws.
   - **home_away_NS** (Positive impact at home): Home advantage improves performance.
   - **rest_days & travel_dist** (Mixed impact): Fatigue and travel can affect performance.

### **Proposed Weighting System**
We assign weights based on impact strength on winning:

| Feature | Weight | Justification |
|---------|--------|--------------|
| **FGM_2** | 0.25 | Directly contributes to scoring |
| **FGM_3** | 0.30 | More valuable than 2-pointers |
| **FTM** | 0.15 | Free points, but lower volume than FGM_3 |
| **AST** | 0.10 | Facilitates high-quality shots |
| **BLK** | 0.05 | Defensive stops prevent opponent scoring |
| **STL** | 0.08 | Creates extra possessions |
| **TOV_team** | -0.12 | Losing possessions hurts scoring |
| **OREB** | 0.10 | Second-chance opportunities boost scoring |
| **DREB** | 0.07 | Limits opponent’s second chances |
| **home_away_NS** | 0.06 | Home advantage improves performance |
| **largest_lead** | 0.20 | Indicates dominance in the game |

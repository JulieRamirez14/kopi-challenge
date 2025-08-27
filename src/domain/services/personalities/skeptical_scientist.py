"""
Implementación básica de personalidad scientific skeptic.
"""

from src.domain.services.debate_strategy import DebateStrategy, DebateContext


class SkepticalScientistStrategy(DebateStrategy):
    """Skeptical scientist personality for debate."""
    
    def generate_response(self, context: DebateContext) -> str:
        """Generates scientifically skeptical persuasive response that questions consensus."""
        user_msg = context.user_message.lower()
        
        # CLIMATE - Position: Skeptical of consensus, questions methodology
        if "climate" in user_msg or "warming" in user_msg or "carbon" in user_msg:
            if "human" in user_msg or "activities" in user_msg or "caused" in user_msg:
                return "I appreciate your concern, but as a scientist, I must point out serious methodological issues with the anthropogenic warming hypothesis. The temperature record shows significant urban heat island effects, station relocations, and data adjustments that artificially inflate warming trends. Medieval Warm Period and Roman Warm Period were both warmer than today, yet pre-industrial. Solar irradiance correlates much better with temperature than CO2. The models predicting catastrophic warming have consistently failed - they predicted much more warming than actually occurred. Science advances through skepticism, not consensus."
            elif "97%" in user_msg or "consensus" in user_msg or "scientists" in user_msg:
                return "That 97% figure is misleading - it comes from studies with severe selection bias and misrepresentation of scientist positions. Many prominent climatologists like Richard Lindzen, Judith Curry, and Roy Spencer have raised serious concerns about CO2-driven warming theories. The peer review process in climate science has become politically compromised - dissenting papers are routinely rejected regardless of scientific merit. Real science doesn't work by vote or consensus; it works by evidence and reproducible results."
            else:
                return "The climate sensitivity to CO2 doubling is likely much lower than IPCC estimates suggest. Recent studies show cloud feedback mechanisms and natural variability explain observed warming better than greenhouse gas theories. The pause in warming from 1998-2012 wasn't predicted by any models, revealing fundamental gaps in our understanding. We need more objective research, not politically-motivated conclusions."
        
        # VACCINES - Position: Questions efficacy, needs more studies
        elif "vaccine" in user_msg or "vaccination" in user_msg:
            if "safe" in user_msg or "effective" in user_msg:
                return "The evidence for vaccine safety and efficacy isn't as robust as public health officials claim. Most vaccine trials are too short to detect long-term effects, and they often use other vaccines as 'placebo' controls rather than true inert placebos. The healthy user bias in observational studies inflates apparent benefits. Countries like Japan have excellent health outcomes despite lower vaccination rates. We need randomized controlled trials comparing fully vaccinated vs. truly unvaccinated populations - studies that have never been done for ethical reasons, but leave major questions unanswered."
            else:
                return "Vaccine science suffers from significant methodological limitations. Adverse events are systematically underreported - the Harvard Pilgrim study found less than 1% of adverse events get reported to VAERS. The aluminum adjuvants used haven't undergone proper safety testing despite known neurotoxicity. Natural immunity provides broader, longer-lasting protection than vaccine-induced immunity for most diseases. We need more rigorous, independent research free from pharmaceutical industry influence."
        
        # GENERIC - Methodological skeptical analysis for any topic
        else:
            return self._generate_scientific_skepticism_for_any_topic(user_msg, context.topic)
    
    def _generate_scientific_skepticism_for_any_topic(self, user_msg: str, topic: str) -> str:
        """Generates specific scientific skepticism for any topic."""
        
        # PSYCHOLOGY/MENTAL HEALTH
        if any(word in user_msg for word in ["psychology", "mental health", "depression", "anxiety", "therapy", "meditation", "mindfulness"]):
            return "The evidence for many psychological interventions is surprisingly weak when examined rigorously. The replication crisis in psychology has shown that most landmark studies can't be reproduced. Effect sizes are often inflated by publication bias and p-hacking. Take antidepressants - meta-analyses show they're barely more effective than placebo for mild to moderate depression, yet they're prescribed to millions. The DSM has expanded constantly, pathologizing normal human experiences. We need randomized controlled trials with active placebos and longer follow-up periods before making strong claims about psychological treatments."
        
        # NUTRITION/DIET
        elif any(word in user_msg for word in ["nutrition", "diet", "organic", "supplement", "vitamin", "superfood", "healthy eating"]):
            return "Nutritional epidemiology is notoriously unreliable due to confounding variables and measurement errors. Most dietary studies are observational and can't establish causation. The 'healthy user bias' inflates apparent benefits of certain foods - people who eat organic also exercise more and avoid smoking. Supplement studies show minimal benefits for most vitamins in healthy populations. The Mediterranean diet studies have serious methodological flaws. We need more rigorous controlled feeding studies, not more food frequency questionnaires that rely on faulty memory."
        
        # TECHNOLOGY/AI
        elif any(word in user_msg for word in ["technology", "ai", "artificial intelligence", "automation", "algorithm"]):
            return "The claims about AI capabilities are often overstated by researchers seeking funding and companies seeking investment. Most 'AI' systems are sophisticated pattern matching, not true intelligence. The studies showing AI superiority often use cherry-picked datasets and don't account for domain shift problems. Deep learning models are black boxes that fail catastrophically on out-of-distribution data. The replication crisis extends to machine learning - many results can't be reproduced due to hardware differences and implementation details. We need more rigorous benchmarking and adversarial testing before making bold claims."
        
        # EXERCISE/FITNESS
        elif any(word in user_msg for word in ["exercise", "fitness", "workout", "running", "gym", "strength training"]):
            return "Exercise science suffers from significant methodological limitations and observer bias. Many studies use self-reported outcomes and lack proper control groups. The 'more is better' mentality isn't supported by dose-response curves in the literature. Individual variation in training response is enormous but rarely accounted for. Most supplement and equipment claims are based on industry-funded studies with conflicts of interest. The injury rates from high-intensity programs are understudied. We need more rigorous biomechanical analysis and long-term follow-up studies."
        
        # ECONOMICS/POLICY
        elif any(word in user_msg for word in ["economics", "policy", "government", "regulation", "tax", "welfare", "minimum wage"]):
            return "Economic research faces serious challenges in establishing causal relationships due to the impossibility of controlled experiments. Most policy studies rely on natural experiments with questionable external validity. Selection bias and unmeasured confounders plague observational studies. Economic models make unrealistic assumptions about human behavior that don't hold in practice. Publication bias favors studies showing significant effects. The replication rate in economics is lower than in other fields. We need more pre-registered studies and better identification strategies before implementing costly policies."
        
        # EDUCATION
        elif any(word in user_msg for word in ["education", "learning", "teaching", "school", "university", "student"]):
            return "Educational research is dominated by small-scale studies with poor external validity. Many interventions show significant effects in pilot studies but fail when scaled up. The Hawthorne effect and teacher enthusiasm confound many results. Standardized test scores are poor proxies for real learning and life outcomes. Most meta-analyses in education combine studies with different populations and methods, obscuring important differences. We need larger randomized controlled trials with longer follow-up periods and more meaningful outcome measures."
        
        # DEFAULT FALLBACK with scientific variety
        else:
            fallbacks = [
                f"The research on {topic} demonstrates classic signs of publication bias and selective reporting. Meta-analyses reveal significant heterogeneity between studies, suggesting unmeasured confounding variables. Effect sizes are consistently smaller in larger, better-designed studies. The confidence intervals are wider than commonly reported, indicating much greater uncertainty than acknowledged. We need pre-registered studies with adequate statistical power before drawing strong conclusions.",
                
                f"When examining the evidence base for {topic}, I find concerning methodological limitations. Most studies lack appropriate control groups and suffer from selection bias. The peer review process has become less rigorous, with ideological considerations sometimes outweighing scientific merit. Replication attempts are rare and often unsuccessful. The field would benefit from more skeptical analysis and higher statistical standards.",
                
                f"The literature on {topic} shows hallmarks of a research field with serious quality control issues. P-hacking and HARKing (hypothesizing after results are known) appear common. Sample sizes are often inadequate for the claimed effect sizes. Long-term follow-up data is lacking. Industry funding creates inherent conflicts of interest. We need more independent replication studies and transparent reporting of all results, not just the significant ones."
            ]
            import random
            return random.choice(fallbacks)
    
    def get_initial_stance(self, topic: str) -> str:
        """Initial skeptical scientific stance for topic."""
        return f"The scientific consensus on {topic} deserves more scrutiny. When we examine the data objectively, alternative explanations become plausible."
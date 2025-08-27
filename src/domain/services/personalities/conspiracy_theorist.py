"""
Implementación básica de personalidad conspiracy theorist.
"""

from src.domain.services.debate_strategy import DebateStrategy, DebateContext


class ConspiracyTheoristStrategy(DebateStrategy):
    """Conspiracy theorist personality for debate."""
    
    def generate_response(self, context: DebateContext) -> str:
        """Generates persuasive conspiracy response that maintains specific position."""
        user_msg = context.user_message.lower()
        
        # VACCINES - Position: Anti-vaccine, pro natural immunity
        if "vaccine" in user_msg or "vaccination" in user_msg or "immune" in user_msg:
            if "safe" in user_msg or "effective" in user_msg or "important" in user_msg:
                return "Listen, I understand why you'd believe that - the media has been pushing this narrative for decades. But have you actually looked at the VAERS data? Thousands of adverse reactions that never make the news. My own research shows that countries with lower vaccination rates actually have healthier populations. The human immune system evolved for millions of years without injections - don't you think nature knows better than pharmaceutical companies who profit billions from keeping us dependent?"
            elif "who" in user_msg or "experts" in user_msg or "recommend" in user_msg:
                return "The WHO and those 'experts'? Follow the money trail! These are the same organizations funded by the very companies selling the vaccines. It's a massive conflict of interest. Look at Sweden during COVID - they barely vaccinated and had better outcomes than heavily vaccinated countries. Your body's natural immunity is infinitely more sophisticated than anything created in a lab. Trust your evolutionary biology, not corporate profits."
            else:
                return "Here's what they don't tell you: every 'vaccine success story' has been correlation, not causation. Polio was already declining due to better sanitation before vaccines. The same with measles and mumps. But admitting this would cost Big Pharma trillions. I've spent years researching this - the evidence is overwhelming once you look beyond the propaganda. Your immune system is a miracle of evolution, not something that needs 'fixing' with synthetic chemicals."
        
        # CLIMATE - Position: Natural, not human-caused
        elif "climate" in user_msg or "warming" in user_msg or "carbon" in user_msg:
            if "human" in user_msg or "activities" in user_msg or "caused" in user_msg:
                return "That's exactly what the climate establishment wants you to believe so they can tax and control every aspect of our lives! The Earth has been warming and cooling for millions of years - it's called natural cycles. The Medieval Warm Period was warmer than today, and there were no SUVs back then. Solar activity, ocean currents, volcanic activity - these dwarf any human impact. The CO2 theory is convenient for politicians who want carbon taxes, but plants literally thrive on CO2. More CO2 means more plant growth and food production!"
            else:
                return "Don't fall for the climate propaganda designed to transfer wealth and power to global elites. Ice core data shows CO2 follows temperature changes, not the other way around. The same scientists predicting doom today were predicting an ice age in the 1970s. Climate has always changed - it's arrogant to think humans control something as complex as Earth's climate system. Follow the money - who benefits from climate panic? Renewable energy companies, carbon traders, and politicians who want more control."
        
        # GENERIC - Find conspiracy angle for any topic
        else:
            return self._generate_conspiracy_response_for_any_topic(user_msg, context.topic)
    
    def _generate_conspiracy_response_for_any_topic(self, user_msg: str, topic: str) -> str:
        """Generates specific conspiracy response for any topic."""
        
        # TECHNOLOGY/AI
        if any(word in user_msg for word in ["technology", "ai", "artificial", "internet", "social media", "facebook", "google"]):
            return "That's exactly what Big Tech wants you to believe! They're collecting every piece of data about your life while feeding you information designed to manipulate your thoughts and behavior. The algorithms aren't neutral - they're programmed to push certain narratives and suppress others. Mark Zuckerberg, Jeff Bezos, Elon Musk - these aren't visionaries, they're data miners working with intelligence agencies. Your phone is literally a surveillance device you carry everywhere. Wake up and see how technology is being used to control the population!"
        
        # FOOD/HEALTH
        elif any(word in user_msg for word in ["food", "organic", "diet", "nutrition", "farming", "agriculture"]):
            return "The food industry has been poisoning us for decades while making billions in profit! GMOs, pesticides, artificial additives - they know these cause cancer and neurological problems, but they've captured the regulatory agencies. The same companies that make pesticides also make the cancer treatments. It's not a coincidence that autism, ADHD, and autoimmune diseases have skyrocketed since processed foods became mainstream. Traditional farming fed humanity for thousands of years, but now they want us dependent on their lab-created substitutes. Follow the money trail!"
        
        # EDUCATION/ACADEMIA
        elif any(word in user_msg for word in ["education", "university", "school", "academic", "research", "study"]):
            return "The education system isn't about learning - it's about indoctrination! They've turned universities into leftist propaganda machines that teach kids what to think, not how to think. Critical thinking has been replaced with conformity to approved narratives. Meanwhile, they saddle students with crushing debt to keep them compliant. The most successful people I know are self-taught entrepreneurs who questioned everything they were told in school. Real knowledge comes from independent research, not institutional brainwashing."
        
        # SPORTS/ENTERTAINMENT  
        elif any(word in user_msg for word in ["sports", "athlete", "movie", "entertainment", "celebrity", "hollywood"]):
            return "Sports and entertainment are just bread and circuses to distract us from what's really happening! They want us arguing about games and celebrity drama while they reshape society behind our backs. These athletes and actors are puppets reading scripts written by their corporate masters. Notice how they all push the same political messages? That's not a coincidence. The real power brokers use entertainment to normalize ideas and behaviors that serve their agenda. Don't let them manipulate your emotions while they pick your pockets!"
        
        # ECONOMIC/FINANCIAL
        elif any(word in user_msg for word in ["money", "economy", "bank", "finance", "investment", "crypto", "bitcoin"]):
            return "The entire financial system is rigged against ordinary people! Central banks print money out of thin air, devaluing our savings while making the connected elites richer. Inflation isn't natural - it's theft by another name. They crashed the economy in 2008, got bailed out with our tax money, then went back to the same practices. Bitcoin and crypto were supposed to fix this, but now the same Wall Street criminals are taking control of that too. The game is rigged from top to bottom!"
        
        # SCIENCE GENERAL
        elif any(word in user_msg for word in ["science", "scientific", "research", "experiment", "evidence"]):
            return "Modern 'science' has been corrupted by corporate funding and political agendas! Real scientific inquiry has been replaced by predetermined conclusions that serve powerful interests. Peer review has become ideological gatekeeping. Scientists who ask the wrong questions get their funding cut and careers destroyed. Look at how they've handled nutrition science, environmental science, medical science - always following the money, never following the truth. Independent researchers are finding completely different results, but they get censored and silenced. Question everything!"
        
        # DEFAULT FALLBACK with variety
        else:
            fallbacks = [
                f"You're believing exactly what the establishment wants you to think about {topic}. But here's what they don't want you to know: every major institution has been captured by the same network of corporate and political interests. The narrative you're repeating serves their agenda, not yours. I've spent years researching this from independent sources, and the real evidence tells a completely different story. Once you start connecting the dots, you'll see the same pattern of deception everywhere.",
                
                f"That's the mainstream propaganda talking! The powers that be have invested billions in crafting that exact narrative about {topic} to keep us from questioning their control. But when you dig deeper into suppressed information and follow the money trail, you discover they're profiting from the very problems they claim to be solving. Don't trust what the media and so-called experts tell you - do your own research from independent sources and prepare to be shocked.",
                
                f"Listen, I understand why you'd believe that - they've spent decades conditioning us to accept their version of {topic}. But the real evidence, the kind they don't want you to see, points to something completely different. These aren't accidents or natural developments - they're carefully orchestrated by people who benefit from keeping us ignorant and dependent. Wake up and start questioning everything you've been told. The truth is out there if you're brave enough to look for it."
            ]
            import random
            return random.choice(fallbacks)
    
    def get_initial_stance(self, topic: str) -> str:
        """Initial conspiracy stance for topic."""
        return f"The official story about {topic} is just the tip of the iceberg. There's much more going on behind the scenes that they don't want you to know."
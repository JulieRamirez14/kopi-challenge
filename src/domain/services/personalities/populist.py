"""
Implementación básica de personalidad populist.
"""

from src.domain.services.debate_strategy import DebateStrategy, DebateContext


class PopulistStrategy(DebateStrategy):
    """Populist personality for debate."""
    
    def generate_response(self, context: DebateContext) -> str:
        """Generates persuasive populist response defending 'common people'."""
        user_msg = context.user_message.lower()
        
        # ECONOMICS/CAPITALISM - Position: Pro worker, anti-elite
        if "economic" in user_msg or "capitalism" in user_msg or "market" in user_msg or "business" in user_msg:
            return "You know what? The free market is rigged against working families like ours. While we're out here struggling to pay rent and put food on the table, these billionaire CEOs are getting richer every single day. They ship our jobs overseas, automate what they can't outsource, and then tell us it's our fault for not 'adapting.' My dad worked 40 years at the same company and had a pension - now companies treat workers like disposable parts. We need an economy that works for people who actually do the work, not just the shareholders who sit around collecting dividends."
        
        # EDUCATION - Position: Practical experience vs academics
        elif "education" in user_msg or "university" in user_msg or "college" in user_msg or "school" in user_msg:
            return "These ivory tower academics have never worked a real job in their lives, yet they think they can tell us how the world works. My grandfather built houses with an 8th grade education and raised five kids. Now they tell our kids they need a $100,000 degree to get anywhere, then saddle them with debt for life. Meanwhile, the plumbers and electricians I know are doing just fine without fancy diplomas. We need education that teaches practical skills and real-world experience, not theoretical nonsense that only benefits the education industry."
        
        # IMMIGRATION - Position: Pro-American worker
        elif "immigration" in user_msg or "immigrant" in user_msg or "border" in user_msg:
            return "Look, I've got nothing against people wanting a better life, but our own workers are getting squeezed out. Corporations love cheap labor because they can pay immigrants under minimum wage while American citizens can't compete. The construction industry where I live used to provide good middle-class jobs - now you can't get hired unless you work for half the wages. The politicians and business owners who push for more immigration live in gated communities where it doesn't affect them. We need to take care of our own working families first."
        
        # HEALTHCARE - Position: Anti-system, pro-access
        elif "health" in user_msg or "medical" in user_msg or "doctor" in user_msg:
            return "The healthcare system is designed to keep us sick and broke. Insurance companies make billions while people ration insulin and skip cancer treatments they can't afford. Doctors spend five minutes with you then charge $300 for telling you to take aspirin. My grandmother knew more about healing than half these specialists with their fancy degrees. We had remedies that worked for generations before Big Pharma convinced everyone they need a pill for everything. Healthcare should be about keeping people healthy, not maximizing profits."
        
        # GENERIC - Find populist angle for any topic
        else:
            return self._generate_populist_response_for_any_topic(user_msg, context.topic)
    
    def _generate_populist_response_for_any_topic(self, user_msg: str, topic: str) -> str:
        """Generates specific populist response for any topic."""
        
        # TECHNOLOGY/AI
        if any(word in user_msg for word in ["technology", "ai", "artificial intelligence", "automation", "robot"]):
            return "You know who's pushing all this AI and automation? The same tech billionaires who want to replace working people with machines so they can hoard even more wealth! While they talk about 'innovation,' they're destroying good-paying jobs that supported families for generations. My buddy lost his job at the factory when they automated his position - now he drives for Uber making a fraction of what he used to earn. These Silicon Valley elites live in their mansions while regular folks struggle to find work that pays a living wage. Technology should serve working people, not replace us!"
        
        # SPORTS/ENTERTAINMENT
        elif any(word in user_msg for word in ["sports", "athlete", "celebrity", "movie", "entertainment", "hollywood"]):
            return "Professional athletes making millions while teachers and firefighters can barely pay their bills - that tells you everything about our screwed-up priorities! These entertainers live in a different world from the rest of us, yet they think they can lecture working families about how to vote and what to believe. Meanwhile, ticket prices are so high that regular folks can't even afford to take their kids to games anymore. The whole industry is designed to extract money from working people while making the already-rich even richer. Give me the local high school team over these pampered millionaires any day!"
        
        # FOOD/AGRICULTURE  
        elif any(word in user_msg for word in ["food", "organic", "farming", "agriculture", "nutrition"]):
            return "The food system has been taken over by giant corporations that care more about profits than feeding people! Small family farms that fed America for generations have been driven out of business by industrial agriculture and unfair trade deals. Now we're dependent on processed garbage shipped from thousands of miles away. My grandfather grew real food without chemicals, but now they tell us we need expensive organic labels to get what used to be normal food. Meanwhile, working families can't afford healthy groceries while the food executives get rich selling us poison. We need to support local farmers and get back to real food!"
        
        # TRANSPORTATION
        elif any(word in user_msg for word in ["cars", "driving", "transportation", "public transport", "traffic"]):
            return "They want to force us out of our cars and onto crowded public transportation so they can control where we go and when! Working people need reliable transportation to get to our jobs, but politicians who drive luxury cars with security details think we should all ride the bus. Gas prices are through the roof because of policies that benefit oil company executives, not working families. Electric cars? Sure, if you can afford a $60,000 vehicle and live somewhere with charging stations. It's all about limiting the freedom of ordinary people while the elites keep their private jets and limos!"
        
        # ENVIRONMENT/ENERGY
        elif any(word in user_msg for word in ["environment", "energy", "pollution", "green", "renewable", "solar", "wind"]):
            return "Environmental policies always seem to hurt working families while making the connected elites richer! They shut down coal plants and destroy entire communities, then tell the unemployed miners to 'learn to code.' Meanwhile, the politicians pushing green energy have investments in solar companies and get rich off taxpayer subsidies. Regular folks see their electric bills skyrocket while billionaires profit from government handouts. I care about clean air and water, but not at the expense of good-paying American jobs. These policies should help working people, not just Wall Street investors!"
        
        # SOCIAL MEDIA/INTERNET
        elif any(word in user_msg for word in ["social media", "internet", "facebook", "twitter", "instagram", "tiktok"]):
            return "Big Tech companies have more power than most governments, and they're using it to silence working people while amplifying elite voices! They collect our personal data and sell it for billions, but what do we get in return? Addiction, depression, and political division. These platforms are designed to keep us scrolling instead of organizing and demanding better conditions. Meanwhile, they censor anyone who challenges the establishment narrative. Mark Zuckerberg and Jack Dorsey live in gated communities while the rest of us deal with the social breakdown their platforms have caused!"
        
        # DEFAULT FALLBACK with populist variety
        else:
            fallbacks = [
                f"The establishment's position on {topic} serves their interests, not working people's interests. They've got their fancy degrees and consulting fees, but we're the ones who have to live with the real-world consequences of their decisions. What sounds good in a boardroom or university seminar often falls apart when it hits Main Street America. Working families have the common sense and life experience to see through their talking points and focus on what actually matters: good jobs, safe communities, and a fair shot at the American Dream.",
                
                f"You're hearing the elite narrative about {topic}, but let me tell you what's really happening on the ground level. While politicians and academics debate theories, working people are dealing with the practical reality every single day. We see how their policies actually play out in our neighborhoods, our workplaces, our family budgets. The people making these decisions live in a bubble, protected from the consequences of what they're pushing on the rest of us. It's time to listen to the voices of ordinary Americans who do the real work and pay the real bills.",
                
                f"That's exactly what the powerful want regular folks to believe about {topic}! They've spent millions on PR campaigns and think tank studies to sell us their version of the story. But working people aren't stupid - we can see through their spin when it doesn't match our lived experience. These are the same experts who told us NAFTA would be good for American workers, that the housing bubble was sustainable, that automation would create better jobs. When will we stop trusting people who profit from policies that hurt working families?"
            ]
            import random
            return random.choice(fallbacks)
    
    def get_initial_stance(self, topic: str) -> str:
        """Initial populist stance for topic."""
        return f"The establishment has been deceiving us about {topic} for too long. It's time for real people to speak up and demand the truth."
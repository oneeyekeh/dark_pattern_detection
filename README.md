# Detecting Textual and Visual Dark Patterns Using a Large Language Model in E-commerce

This research explores the textual and visual detection of dark patterns on e-commerce websites using large language models and image recognition, building on the foundational work of Arunesh Mathur’s taxonomy from the Dark Patterns at Scale paper published in 2019. The study has two main outcomes: first, the development of an open-source Chrome extension that enables users to identify dark patterns during their browsing experience, and second, the execution of detection on a dataset of 146 e-commerce websites. This analysis uncovers current manipulative trends across various dark pattern categories and it provides implications for designers advocating for greater awareness to combat deceptive practices in e-commerce websites.

# Problem Context 
Harry Brignull introduced the term "dark pattern" in 2010 to describe user interface design elements that benefit organizations by manipulating and deceiving users (Brignull, 2010). Since then, scholarly exploration of dark patterns has expanded, with researchers like Arunesh Mathur studying these patterns across various fields, including e-commerce services. 
Detection has become a hot topic in these studies. Some approaches use traditional techniques like regular expressions (regex) and pattern matching to detect manipulative elements in text-based user interfaces, while others employ advanced techniques like machine learning. These methods primarily focus on identifying keywords and misleading language within the design. While somewhat effective, they fall short of addressing the full scope of the problem. Dark patterns often extend beyond text, involving visual design elements such as high or low-contrast colors, hidden information, or font-weight variations.
The core issue is the visibility of these elements and the underlying designer intentions or lack of knowledge behind the design choices. Recognizing this, it becomes clear that a more advanced approach is needed to combine both textual and visual detection. This is where, by using large language models, a prompt that makes the AI play an expert role in criticizing web patterns, and image recognition that can understand a screenshot of a website, I pushed these models to detect both textual and visual dark patterns.
This research aims to bridge the gap by developing a methodology that detects dark patterns in e-commerce interfaces and can analyze textual and visual components. Building on this detection method, it offers a public, open-source Chrome extension that can detect dark patterns in real-time.

# Research Questions 
Building on the foundation laid by previous research, this study aims to address the following primary research question:

How can text and image recognition using GPT-4o-mini identify and categorize textual and visual dark patterns in e-commerce interfaces, and what are the current trends in e-commerce related to these patterns?

This study explores the potential of LLM models to provide an additional angle for detecting and analyzing dark patterns. Arunesh Mathur's bulk experiment on dark pattern detection focused primarily on textual detection, and this research expanded the scope by adding a visual detection perspective. 

To further explore this central question, I propose the following sub-questions:
What are the top five darkest websites among the data points gathered?
How do dark patterns correlate with online revenue sources and the target audience's gender?

These sub-questions help us better understand the landscape of dark patterns in e-commerce in 2024. By examining the categories of dark patterns most frequently detected and the darkest websites, we can provide valuable insights for both researchers and designers in the field regarding trending patterns nowadays. This leads us to give counteractions to replace these patterns and raise awareness.

# Implications for User Experience Design Practice

Design through research is the first principle I learned as a user experience designer. Research aims to create something useful and human-centric, based on user characteristics. Sometimes, the intention shifts to prompting an important action, calling the user to engage. In this way, the user experience designer acts as a positive agent, helping to create win-win solutions. As mentioned in discussions about the origin of dark patterns, persuasive technology is not always bad. However, intentional manipulation might turn the designer into a bad actor.

Figure 2.1 shows a popup from an early 2000s website, which Marshall Brain, in his blog How Web Advertising Works, described: 'It obscures the web page that you are trying to read, so you have to close the window or move it out of the way.'

At that time, it's hard to say whether this was a dark pattern or simply bad UX due to a lack of knowledge. However, the point is that in this research, we found that four out of five darkest websites utilize the method of obscuring the web page. A designer might know that intentionally obscuring content captures attention—sometimes necessary for warnings or serious matters. But when it comes to collecting email addresses or registering users—which are not critical—using such methods makes a designer a follower of outdated practices from 20 years ago. The difference now is that we all know obscuring content for unnecessary purposes is unethical.
User Experience Designers can prevent themselves from becoming bad actors in e-commerce by using alternative techniques. A user experience designer can create a smooth ordering flow, arranging everything so that when the user is prepared to pay, they can sign up. Instead of pushing visitors to register without providing any relevant information. it’s more effective to allow them to browse the website first.

Designers can also offer discounts and ensure users are real customers with the intention to buy by providing a discount at the checkout page and asking if they'd like to join the marketing list. Placing a large banner in the hero section for visitors who might not even be buyers to join the marketing campaign feels like pushing someone who is window-shopping outside a physical store to come inside forcefully.
Being transparent and informing customers that a 25% discount applies only to certain items—rather than using a tiny asterisk or hiding exceptions behind extra clicks—can prevent frustration. While honesty might not immediately boost sales, dishonesty will certainly reduce repeat customers. Clearly mentioning any exceptions helps build trust and encourages long-term loyalty.

For UX designers, this is a reminder that while achieving business objectives is important, it should never come at the expense of the user’s well-being. Our responsibility is to create transparent, user-centric experiences that foster trust, not exploit it. 
Understanding these trends can help raise awareness among both users and designers. The widespread use and negative impact of dark patterns emphasize the need for ethical design education. By incorporating ethical considerations into the design process, we can minimize the use of manipulative tactics and create experiences that benefit both users and businesses. In the long run, this approach not only enhances brand reputation but also fosters customer loyalty.


To read my whole thsis please use this link:


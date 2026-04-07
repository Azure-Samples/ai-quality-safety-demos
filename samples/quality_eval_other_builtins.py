import rich
from azure.ai.evaluation import (
    BleuScoreEvaluator,
    F1ScoreEvaluator,
    GleuScoreEvaluator,
    MeteorScoreEvaluator,
    RougeScoreEvaluator,
    RougeType,
)

context = 'Dining chair. Wooden seat. Four legs. Backrest. Brown. 18" wide, 20" deep, 35" tall. Holds 250 lbs.'
query = "Given the product specification for the Contoso Home Furnishings Dining Chair, provide an engaging marketing product description."
ground_truth = 'The dining chair is brown and wooden with four legs and a backrest. The dimensions are 18" wide, 20" deep, 35" tall. The dining chair has a weight capacity of 250 lbs.'
response = 'Introducing our timeless wooden dining chair, designed for both comfort and durability. Crafted with a solid wood seat and sturdy four-legged base, this chair offers reliable support for up to 250 lbs. The smooth brown finish adds a touch of rustic elegance, while the ergonomically shaped backrest ensures a comfortable dining experience. Measuring 18" wide, 20" deep, and 35" tall, it\'s the perfect blend of form and function, making it a versatile addition to any dining space. Elevate your home with this beautifully simple yet sophisticated seating option.'

f1_eval = F1ScoreEvaluator()
f1_score = f1_eval(response=response, ground_truth=ground_truth)
rich.print(f1_score)

rouge_eval = RougeScoreEvaluator(rouge_type=RougeType.ROUGE_1)
rouge_score = rouge_eval(response=response, ground_truth=ground_truth)
rich.print(rouge_score)

bleu_eval = BleuScoreEvaluator()
bleu_score = bleu_eval(response=response, ground_truth=ground_truth)
rich.print(bleu_score)

meteor_eval = MeteorScoreEvaluator(alpha=0.9, beta=3.0, gamma=0.5)
meteor_score = meteor_eval(response=response, ground_truth=ground_truth)
rich.print(meteor_score)


gleu_eval = GleuScoreEvaluator()
gleu_score = gleu_eval(response=response, ground_truth=ground_truth)
rich.print(gleu_score)

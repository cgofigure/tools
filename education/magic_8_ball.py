import random

def magic_8_ball():
    answers = [
      "Yes - definitely.",
      "It is decidedly so.",
      "Without a doubt.",
      "Reply hazy, try again.",
      "Ask again later.",
      "Better not tell you now.",
      "My sources say no.",
      "Outlook not so good.",
      "Very doubtful."
    ]

    input("What is your question? ")
    answer = random.choice(answers)
    print(answer)
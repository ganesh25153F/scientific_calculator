from calculator import ScientificCalculator
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()

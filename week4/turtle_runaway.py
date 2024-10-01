import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, root, canvas, runner, chaser, catch_radius=40):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2 
        self.start_time = 0
        self.game_over = False
        self.score = 0  

        self.timer_display = turtle.RawTurtle(canvas)
        self.timer_display.hideturtle()
        self.timer_display.penup()
        self.timer_display.setpos(0, 320)

        self.score_display = turtle.RawTurtle(canvas)
        self.score_display.hideturtle()
        self.score_display.penup()
        self.score_display.setpos(-300, 320)

        self.smiley = turtle.RawTurtle(canvas)
        self.smiley.shape('circle') 
        self.smiley.color('yellow')
        self.smiley.penup()
        self.smiley.setpos(random.randint(-300, 300), random.randint(-300, 300))

        # 거북이 설정
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        
    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2 

    def runner_eat_smiley(self):
        p = self.runner.pos()
        q = self.smiley.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < 400 

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.start_time = time.time()
        self.ai_timer_msec = ai_timer_msec

        self.update_score()

        self.canvas.after(self.ai_timer_msec, self.step)
        self.update_timer()

    def step(self):
        if self.game_over:
            return  

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        if self.runner_eat_smiley():
            self.score += 1 
            self.update_score()  

            self.smiley.setpos(random.randint(-300, 300), random.randint(-300, 300))

        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}')

        if is_catched:
            elapsed_time = time.time() - self.start_time
            self.drawer.setpos(0, 0)
            self.drawer.write(f"Game Over! score: {int(self.score)}", align="center", font=("Arial", 24, "normal"))
            self.game_over = True 
            self.runner.stop_movement()  
            self.chaser.stop_movement() 
        else:
            self.canvas.after(self.ai_timer_msec, self.step)

    def update_timer(self):
        if self.game_over:
            return  

        elapsed_time = time.time() - self.start_time
        self.timer_display.undo()  # Clear previous time
        self.timer_display.setpos(0, 320)
        self.timer_display.write(f'Time: {elapsed_time:.1f} sec', align="center", font=("Arial", 16, "normal"))

        self.canvas.after(100, self.update_timer)

    def update_score(self):
        self.score_display.undo() 
        self.score_display.setpos(-300, 320)
        self.score_display.write(f'Score: {self.score}', align="center", font=("Arial", 16, "normal"))
        self.canvas.update() 

class ManualMover(turtle.RawTurtle):
    def __init__(self, root, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.tk_canvas = canvas
        self.step_move = step_move
        self.step_turn = step_turn
        self.game_over = False

        self.key_state = {
            'Up': False,
            'Down': False,
            'Left': False,
            'Right': False
        }

        root.bind('<KeyPress-Up>', lambda event: self.set_key_state('Up', True))
        root.bind('<KeyPress-Down>', lambda event: self.set_key_state('Down', True))
        root.bind('<KeyPress-Right>', lambda event: self.set_key_state('Right', True))
        root.bind('<KeyPress-Left>', lambda event: self.set_key_state('Left', True))

        root.bind('<KeyRelease-Up>', lambda event: self.set_key_state('Up', False))
        root.bind('<KeyRelease-Down>', lambda event: self.set_key_state('Down', False))
        root.bind('<KeyRelease-Left>', lambda event: self.set_key_state('Left', False))
        root.bind('<KeyRelease-Right>', lambda event: self.set_key_state('Right', False))

        self.update_movement()

    def set_key_state(self, key, state):
        if self.game_over:
            return
        self.key_state[key] = state

    def check_boundaries(self):
        x, y = self.pos()
        canvas_width = self.tk_canvas.cv.winfo_width() / 2 
        canvas_height = self.tk_canvas.cv.winfo_height() / 2  

        if x < -canvas_width:
            self.setx(-canvas_width)
        elif x > canvas_width:
            self.setx(canvas_width)

        if y < -canvas_height:
            self.sety(-canvas_height)
        elif y > canvas_height:
            self.sety(canvas_height)

    def update_movement(self):
        if self.game_over:
            return 
        
        if self.key_state['Up']:
            self.forward(self.step_move)
        if self.key_state['Down']:
            self.backward(self.step_move)
        if self.key_state['Left']:
            self.left(self.step_turn)
        if self.key_state['Right']:
            self.right(self.step_turn)

        self.check_boundaries()

        self.getscreen().ontimer(self.update_movement, 50)
    
    def stop_movement(self):
        self.game_over = True

    def run_ai(self, opp_pos, opp_heading):
        pass


class ChaserMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=20, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
    
    def run_ai(self, opp_pos, opp_heading):
        x, y = self.pos()  
        opp_x, opp_y = opp_pos

        angle_to_runner = self.towards(opp_x, opp_y)
        self.setheading(angle_to_runner)
        self.forward(self.step_move)

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()

    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("lightblue") 
    
    runner = ManualMover(root, screen)
    chaser = ChaserMover(screen)

    game = RunawayGame(root, canvas, runner, chaser)
    game.start()
    root.mainloop()

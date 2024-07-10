import random
import pygame
from game import Robot, Grid, Robot_game

type Individual = list[str]

class GeneticAlgorithm:
    def __init__(self, population_size : int, mutation_rate: float,
                crossover_rate: float, max_generations: int, grid: list[list[str]], max_commands: int) -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations
        self.grid = grid
        self.max_commands = max_commands
        self.commands = ["Turn Left", "Turn Right", "Move Forward"]


    def create_individual(self) -> Individual:
        return [random.choice(self.commands) for _ in range(self.max_commands)]


    def create_population(self) -> list[Individual]:
        return [self.create_individual() for _ in range(self.population_size)]


    def evaluate_individual(self, individual: Individual) -> float:
        robot = Robot(self.grid)
        for command in individual:
            if command == "Turn Left":
                robot.turn_left()
            elif command == "Turn Right":
                robot.turn_right()
            elif command == "Move Forward":
                robot.move_forward()
                if self.grid.grid[robot.y][robot.x] == '2':
                    break
            if self.grid.grid[robot.y][robot.x] == '#':
                return 0

        goal_position = self.find_goal_position()
        distance_to_goal = abs(robot.x - goal_position[0]) + abs(robot.y - goal_position[1])
        return distance_to_goal


    def find_goal_position(self) -> tuple[int, int]:
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if self.grid.grid[row][col] == '#':
                    return col, row


    def select_individual(self, population: list[Individual], fitnesses: list[float]) -> Individual:
        total_fitness = sum(fitnesses)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness in zip(population, fitnesses):
            current += fitness
            if current > pick:
                return individual


    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.max_commands - 1)
            return parent1[:point] + parent2[point:]
        return parent1


    def mutate(self, individual: Individual) -> Individual:
        for i in range(self.max_commands):
            if random.random() < self.mutation_rate:
                individual[i] = random.choice(self.commands)
        return individual


    def run(self) -> Individual | None:
        population = self.create_population()
        for generation in range(self.max_generations):
            fitnesses = [self.evaluate_individual(ind) for ind in population]
            new_population = []

            for _ in range(self.population_size):
                parent1 = self.select_individual(population, fitnesses)
                parent2 = self.select_individual(population, fitnesses)
                offspring = self.crossover(parent1, parent2)
                offspring = self.mutate(offspring)
                new_population.append(offspring)

            population = new_population

            best_individual = min(population, key=self.evaluate_individual)
            best_fitness = self.evaluate_individual(best_individual)

            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

            if best_fitness == 0:
                print("Solution found!")
                return best_individual

        print("No solution found.")
        return None


class Robot_game_with_ml(Robot_game):


    def __init__(self) -> None:
        super().__init__()


    def init_level(self) -> None:
        MAX_COMMANDS = 20
        grid = Grid("assets/level.txt", 50)
        
        ga = GeneticAlgorithm(
            population_size=300,
            mutation_rate=0.01,
            crossover_rate=0.7,
            max_generations=100,
            grid=grid,
            max_commands=MAX_COMMANDS
        )

        best_solution = ga.run()

        if best_solution is not None:
            print("Best Solution:", best_solution)
            self.play_solution(grid, best_solution, MAX_COMMANDS)
        else:
            print("Failed to find a solution")
    

    def play_solution(self, grid, solution, max_commands) -> None:
        robot = Robot(grid)
        for command in solution:
            if command == "Turn Left":
                robot.turn_left()
            elif command == "Turn Right":
                robot.turn_right()
            elif command == "Move Forward":
                robot.move_forward()
                if grid.grid[robot.y][robot.x] == '2':
                    self.initialize_failure_giu()

            grid.draw(self.screen)
            robot.draw(self.screen)
            pygame.display.update()
            pygame.time.delay(600)

        if grid.grid[robot.y][robot.x] == '#':
            self.initialize_sucess_gui(score=len(solution), max_commands=max_commands)
        else:
            self.initialize_failure_giu()
    
        print(solution)


Robot_game_with_ml().init_game()
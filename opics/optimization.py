import numpy as np


class Particle:
    """
    Represents a Particle inside a Swarm.

    Args:
        dim_shape (int): Number of dimensions to optimize.
        pos_bounds (tuple): Min and Max values for each dimension.
        vel_bounds (tuple): Min and Max values for velocity.
    """

    def __init__(self, dim_shape, pos_bounds, vel_bounds):
        self.pos = np.array([np.random.uniform(_[0], _[1]) for _ in pos_bounds])
        self.vel = np.random.uniform(vel_bounds[0], vel_bounds[1], dim_shape)
        self.pbest = np.inf
        self.pbestpos = np.zeros(dim_shape)


class Swarm:
    """
    Creates a pool/swarm of particles.

    Args:
        num_particles (int): Number of particles.
        dim_shape (tuple): Number of dimensions to optimize.
        pos_bounds (tuple): Min and Max values for position.
        vel_bounds (tuple): Min and Max values for  velocity.
        inertia_weight_bounds (tuple): Min and Max values for interia weight.
        c (tuple):  c[0] -> cognitive parameter, c[1] -> social parameter.
        log_results (tuple): A tuple of boolean values to log best fitness\
            and particle positions, e.g., (True, True).
    """

    def __init__(
        self,
        num_particles=20,
        dim_shape=None,
        pos_bounds=None,
        vel_bounds=None,
        inertia_weight_bounds=(0.4, 0.9),
        c=(1.4944, 1.4944),
        log_results=(True, True),
        tolerance=1e-5,
    ):

        if vel_bounds is None:
            self.vel_bounds = (
                np.array([-1, 1]) * 0.15 * (np.amax(pos_bounds) - np.amin(pos_bounds))
            )
        else:
            self.vel_bounds = vel_bounds

        if len(pos_bounds) != dim_shape or type(pos_bounds[-1]) not in (tuple, list):
            raise ValueError("Min and Max values are not provided for each dimension.")

        self.pool = np.array(
            [
                Particle(dim_shape, pos_bounds, self.vel_bounds)
                for _ in range(num_particles)
            ]
        )
        self.gbest = np.inf
        self.gbestpos = np.zeros(dim_shape)
        self.pos_bounds = pos_bounds
        self.c0 = c[0]
        self.c1 = c[1]
        self.inertia_weight_bounds = inertia_weight_bounds
        self.dim_shape = dim_shape
        self.update_particle_pos = None
        self.update_particle_vel = None

        self.log_flag_fitness = log_results[0]
        self.log_flag_particles = log_results[1]
        self.log_fitness = []
        self.log_all_particles = []
        self.log_best_particles = []
        self.tolerance = tolerance

    def update_particle_position(self, p, fitness):
        """
        Updates particle position.

        Args:
            p (opics.optimization.Particle): Particle.
            fitness (double): fitness value or loss (to be minimized).

        Returns:
            Particle (opics.optimization.Particle)
        """
        if fitness < p.pbest:
            p.pbest = fitness
            p.pbestpos = p.pos

        return p

    def update_particle_velocity(self, p):
        """
        Updates particle velocity.

        Args:
            p (opics.optimization.Particle): Particle.

        Returns:
            Particle (opics.optimization.Particle)
        """
        iw = np.random.uniform(
            self.inertia_weight_bounds[0], self.inertia_weight_bounds[1], self.dim_shape
        )
        p.vel = (
            iw * p.vel
            + (
                self.c0
                * np.random.uniform(0.0, 1.0, self.dim_shape)
                * (p.pbestpos - p.pos)
            )
            + (
                self.c1
                * np.random.uniform(0.0, 1.0, self.dim_shape)
                * (self.gbestpos - p.pos)
            )
        )

        p.vel = p.vel.clip(min=self.vel_bounds[0], max=self.vel_bounds[1])
        p.pos = p.pos + p.vel
        for _ in range(self.dim_shape):
            p.pos[_] = p.pos[_].clip(
                min=self.pos_bounds[_][0], max=self.pos_bounds[_][1]
            )

        return p

    def optimize(self, function, print_step, iterations):
        """
        Starts optimization.

        Args:
            function (function): Function to be optimized/ minimized.
            print_step (int): Steps to print optimization progress after.
            iterations (int): Number of optimization iterations.
        """
        function = np.vectorize(function)
        self.update_particle_pos = np.vectorize(self.update_particle_position)
        self.update_particle_vel = np.vectorize(self.update_particle_velocity)

        for i in range(iterations):
            fitness = function(self.pool)
            self.pool = self.update_particle_pos(self.pool, fitness)
            min_fitness = fitness[np.argmin(fitness)]
            if min_fitness < self.gbest:
                self.gbest = min_fitness
                self.gbestpos = self.pool[np.argmin(fitness)].pos

            if self.log_flag_fitness:
                self.log_fitness.append(self.gbest)
            if self.log_flag_particles:
                self.log_all_particles.append(
                    [[each.pos, each.vel] for each in self.pool]
                )
                self.log_best_particles.append(self.gbestpos)

            self.pool = self.update_particle_vel(self.pool)

            if i % print_step == 0:
                print(
                    f"Iteration: {i}, Loss/gbest: {self.gbest}, Fitness: {min_fitness}"
                )

            if self.gbest <= self.tolerance:
                break

        print("global best fitness: ", self.gbest)

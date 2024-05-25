program CosmicWebSimulation
  implicit none

  ! Constants
  double precision, parameter :: G = 6.67430e-11   ! Gravitational constant (m^3 kg^-1 s^-2)
  double precision, parameter :: H0 = 67.4         ! Hubble constant (km/s/Mpc)
  double precision, parameter :: Omega_m = 0.315   ! Matter density parameter
  double precision, parameter :: Omega_lambda = 0.685 ! Dark energy density parameter

  ! Simulation parameters
  integer, parameter :: n_particles = 1000
  double precision, parameter :: box_size = 100.0  ! Box size in Mpc
  double precision, parameter :: dt = 1e-3         ! Time step in Gyr
  double precision, parameter :: total_time = 13.8 ! Total simulation time in Gyr

  ! Particle properties
  double precision :: mass(n_particles)
  double precision :: position(3, n_particles)
  double precision :: velocity(3, n_particles)
  double precision :: acceleration(3, n_particles)
  double precision :: density(n_particles)
  double precision :: energy(n_particles)

  ! Simulation variables
  double precision :: time
  integer :: i, j
  character(len=100) :: filename

  ! Initialize particles
  call initialize_particles(position, velocity, mass, density, energy)

  ! Main simulation loop
  time = 0.0
  do while (time < total_time)
     call compute_gravitational_acceleration(position, mass, acceleration)
     call update_positions(position, velocity, acceleration, dt)
     call update_velocities(velocity, acceleration, dt)
     call compute_density(position, density)
     call compute_energy(velocity, mass, density, energy)

     ! Create filename for the current timestep
     write(filename, '("output_", F5.2, ".csv")') time
     call output_to_csv(position, density, energy, time, filename)

     time = time + dt
  end do

contains

  subroutine initialize_particles(pos, vel, m, dens, en)
    double precision, intent(out) :: pos(3, n_particles), vel(3, n_particles), m(n_particles)
    double precision, intent(out) :: dens(n_particles), en(n_particles)
    integer :: i

    do i = 1, n_particles
       pos(:, i) = box_size * rand_array(3)
       vel(:, i) = 0.0
       m(i) = 1.0
       dens(i) = 0.0
       en(i) = 0.0
    end do
  end subroutine initialize_particles

  subroutine compute_gravitational_acceleration(pos, m, acc)
    double precision, intent(in) :: pos(3, n_particles), m(n_particles)
    double precision, intent(out) :: acc(3, n_particles)
    double precision :: r(3), dist, force
    integer :: i, j

    acc = 0.0
    do i = 1, n_particles
       do j = 1, n_particles
          if (i /= j) then
             r = pos(:, j) - pos(:, i)
             dist = sqrt(sum(r**2))
             if (dist > 0.0) then
                force = G * m(i) * m(j) / dist**2
                acc(:, i) = acc(:, i) + force * r / dist
             end if
          end if
       end do
    end do
  end subroutine compute_gravitational_acceleration

  subroutine update_positions(pos, vel, acc, dt)
    double precision, intent(inout) :: pos(3, n_particles), vel(3, n_particles)
    double precision, intent(in) :: acc(3, n_particles), dt
    integer :: i

    do i = 1, n_particles
       pos(:, i) = pos(:, i) + vel(:, i) * dt + 0.5 * acc(:, i) * dt**2
    end do
  end subroutine update_positions

  subroutine update_velocities(vel, acc, dt)
    double precision, intent(inout) :: vel(3, n_particles)
    double precision, intent(in) :: acc(3, n_particles), dt
    integer :: i

    do i = 1, n_particles
       vel(:, i) = vel(:, i) + acc(:, i) * dt
    end do
  end subroutine update_velocities

  subroutine compute_density(pos, dens)
    double precision, intent(in) :: pos(3, n_particles)
    double precision, intent(out) :: dens(n_particles)
    integer :: i

    ! Placeholder for density computation
    dens = 1.0
  end subroutine compute_density

  subroutine compute_energy(vel, m, dens, en)
    double precision, intent(in) :: vel(3, n_particles), m(n_particles)
    double precision, intent(in) :: dens(n_particles)
    double precision, intent(out) :: en(n_particles)
    integer :: i

    do i = 1, n_particles
       en(i) = 0.5 * m(i) * sum(vel(:, i)**2) + G * m(i) * dens(i)
    end do
  end subroutine compute_energy

  subroutine output_to_csv(pos, dens, en, t, filename)
    double precision, intent(in) :: pos(3, n_particles), dens(n_particles), en(n_particles), t
    character(len=100), intent(in) :: filename
    integer :: i
    open(unit=10, file=filename, status='replace', action='write')
    write(10, *) 'x, y, z, density, energy, time'
    do i = 1, n_particles
       write(10, '(F12.6, 1x, F12.6, 1x, F12.6, 1x, F12.6, 1x, F12.6, 1x, F12.6)') &
             pos(1, i), pos(2, i), pos(3, i), dens(i), en(i), t
    end do
    close(10)
  end subroutine output_to_csv

  function rand_array(n)
    integer, intent(in) :: n
    double precision :: rand_array(n)
    integer :: i
    call random_seed()
    do i = 1, n
       call random_number(rand_array(i))
    end do
  end function rand_array

end program CosmicWebSimulation

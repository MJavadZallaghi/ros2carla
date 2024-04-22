import carla
import random

# Connect to the client and retrieve the world object
# client = carla.Client('localhost', 2000)
carla_server_ip_file = open("carla_server_ip_file.txt", "r")
carla_server_ip = carla_server_ip_file.readlines()[0].strip()
# print("Carla Server IP: ", carla_server_ip)


client = carla.Client(carla_server_ip, 2000)
client.load_world('Town05')
world = client.get_world()

# Retrieve the spectator object
spectator = world.get_spectator()

# Get the location and rotation of the spectator through its transform
transform = spectator.get_transform()

location = transform.location
rotation = transform.rotation

# Set the spectator with an empty transform

main_cam_tf = carla.Transform()
main_cam_tf.location.z = 150
main_cam_tf.rotation.pitch = -90


spectator.set_transform(main_cam_tf)
# This will set the spectator at the origin of the map, with 0 degrees
# pitch, yaw and roll - a good way to orient yourself in the map

# Get the blueprint library and filter for the vehicle blueprints
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')

# Get the map's spawn points
spawn_points = world.get_map().get_spawn_points()

# Spawn 50 vehicles randomly distributed throughout the map 
# for each spawn point, we choose a random vehicle from the blueprint library
for i in range(0,5):
    world.try_spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))


ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))

# Create a transform to place the camera on top of the vehicle
camera_init_trans = carla.Transform(carla.Location(z=1.5))

# We create the camera through a blueprint that defines its properties
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')

# We spawn the camera and attach it to our ego vehicle
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

# Start camera with PyGame callback
# camera.listen(lambda image: image.save_to_disk('out/%06d.png' % image.frame))


for vehicle in world.get_actors().filter('*vehicle*'):
    vehicle.set_autopilot(True)

for bp in world.get_blueprint_library().filter('vehicle'):
    print(bp.id)

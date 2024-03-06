#include <cmath>
#include <vector>

using namespace std;

const long double G = 6.67408E-11;

vector<long double> calculate_acceleration(long double star_position_x,long double star_position_y,long double star_mass,long double body_position_x,long double body_position_y){
    // Calculates acceleration of body
    long double distance_x = star_position_x - body_position_x;
    long double distance_y = star_position_y - body_position_y;

    long double distance = sqrt(pow(distance_x,2),pow(distance_y,2));

    long double acceleration_x = star_mass*G/pow(distance,3)*distance_x;
    long double acceleration_y = star_mass*G/pow(distance,3)*distance_y;

    vector<long double> acceleration = {acceleration_x,acceleration_y};

    return acceleration;
}

void move_space_objects(int time, vector<vector<long double>> stars_positions, vector<vector<long double>> planets_positions, )

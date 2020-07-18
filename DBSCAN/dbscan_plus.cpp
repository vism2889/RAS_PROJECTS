// AUTHOR: Morgan Visnesky
// DATE: 07/18/20
// FILENAME: dbscan_plus.cpp
//
// DESCRIPTION:
// Beginnings of a C++ implementation of DBSCAN algorithm.
//
# include <iostream>
# include <vector>
# include <math.h>

using namespace std;


class Point
{
public:
  int x;
  int y;
  int z;
  int label;
  std::vector<Point> neighbors;
};

float distFunc(Point a, Point b);
std::vector<Point> regionQuery(std::vector<Point> database, int p, float epsilon);
void growCluster(std::vector<Point> database, std::vector<int> labels, int p, int c, float epsilon, int MinPts);


int main()
{
  std::vector<Point> database;
  for (int i = 0; i < 5; i++)
  {
    Point p;
    p.x = i;
    p.y = i;
    p.z = i;
    database.push_back(p);
    //cout << database[i].x;
  }
  cout << endl;
  for (int i = 0; i < 5;i++)
  {
    //cout << endl;
    //cout << "Hey";
    //cout << endl;
    cout << database[i].x << database[i].y << database[i].z;
    cout << endl;
  }

  cout << "distance function: ";
  cout << "hey " << distFunc(database[2], database[3]);
  cout << endl;
  return 0;
}




float distFunc(Point a, Point b)
{
  float dist = sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y, 2) + pow(b.z-a.z, 2));
  return dist;
}

std::vector<Point> regionQuery(std::vector<Point> database, int p, float epsilon)
{

  std::vector<Point> neighbors;
  for (int i = 0; i <= database.size(); i++)
  {
    if (distFunc(database[p],database[i]) < epsilon)
    {
      neighbors.push_back(database[i]);
    }
  }
  return neighbors;
}

void growCluster(std::vector<Point> database, std::vector<int> labels, int p, int c, float epsilon, int minPts)
{
  std::vector<int> searchQueue;
  int i = 0;
  while (i < searchQueue.size())
  {
    p = searchQueue[i];
    std::vector<Point> neighborPts = regionQuery(database, p, epsilon);
    if (neighborPts.size() < minPts)
    {
      i = i + 1;
    }
  }
}

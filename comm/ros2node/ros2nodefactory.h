#ifndef ROS2NODEFACTORY_H
#define ROS2NODEFACTORY_H

#include <common/nodefactoryinterface.h>
#include <ros2node/ros2node.h>

//TODO - deps to cpp
class Ros2NodeFactory : public NodeFactoryInterface
{
public:
    communication::NodeInterfacePtr makeNode(QString nodeName)
    {
        return communication::NodeInterfacePtr(new roscommunication::Ros2Node(nodeName));
    }
};
typedef QSharedPointer<Ros2NodeFactory> Ros2NodeFactoryPtr;

#endif //ROS2NODEFACTORY_H

from pkg.pyrestorm.models import RestModel

class NodeInfo(RestModel):
    class Meta:
        url = "http://192.168.1.10:8000/nodes/"

    def __repr__(self):
        return '%s - %s -%s ' % (self.node_id, self.positionx, self.positiony)



# 添加
# newnode = NodeInfo(node_id = 10, ip = "192.12.2.1", positionx = 10, positiony = 9)
# newnode.save()

# 修改  X
NodeInfo.objects.filter(id=8).update(positionx = 18)

# 删除  X
# NodeInfo.objects.filter(id=8).delete()


# 查询
nodes = NodeInfo.objects.all()

for node in nodes:
    print(node)


# print(nodes[0])


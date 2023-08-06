"""
模型权重初始化

注意 model.modules() 和 model.children() 的区别：model.modules() 会迭代地遍历模型的所有子层，而 model.children() 只会遍历模型下的一层。

"""
def mode_init(model):
	for layer in model.modules():
	    if isinstance(layer, torch.nn.Conv2d):
	        torch.nn.init.kaiming_normal_(layer.weight, mode='fan_out',
	                                      nonlinearity='relu')
	        if layer.bias is not None:
	            torch.nn.init.constant_(layer.bias, val=0.0)
	    elif isinstance(layer, torch.nn.BatchNorm2d):
	        torch.nn.init.constant_(layer.weight, val=1.0)
	        torch.nn.init.constant_(layer.bias, val=0.0)
	    elif isinstance(layer, torch.nn.Linear):
	        torch.nn.init.xavier_normal_(layer.weight)
	        if layer.bias is not None:
	            torch.nn.init.constant_(layer.bias, val=0.0)

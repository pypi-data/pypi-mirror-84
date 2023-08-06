import torch.nn as nn
import torch


def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    """3x3 convolution with padding"""
    return nn.Sequential(
        nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                  padding=dilation, groups=groups, bias=False, dilation=dilation),
        nn.BatchNorm2d(out_planes),
        nn.LeakyReLU(0.1)
    )


def conv1x1(in_planes, out_planes, stride=1):
    """1x1 convolution"""
    return nn.Sequential(
        nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False),
        nn.BatchNorm2d(out_planes),
        nn.LeakyReLU(0.1)
    )


class _ResidualBlock(nn.Module):
    def __init__(self, num, in_channels, out_channels, downsample=True):
        super(_ResidualBlock, self).__init__()
        self.repeat = num
        self.downsample = downsample
        layers = []
        layers.append(conv1x1(in_channels, in_channels // 2))
        layers.append(conv3x3(in_channels // 2, in_channels))
        self.residual = nn.Sequential(*layers)
        self.conv = conv3x3(in_channels, out_channels, stride=2)

    def forward(self, x):
        for i in range(self.repeat):
            short_cut = x
            x = self.residual(x)
            x = x + short_cut
        self.route = x
        if self.downsample:
            x = self.conv(x)
        return x


class Darknet53(nn.Module):
    def __init__(self):
        super(Darknet53, self).__init__()
        self.conv3_1 = conv3x3(3, 32, 1)
        self.conv3_2 = conv3x3(32, 64, 2)
        self.layer1 = _ResidualBlock(1, 64, 128)
        self.layer2 = _ResidualBlock(2, 128, 256)
        self.layer8_1 = _ResidualBlock(8, 256, 512)
        self.layer8_2 = _ResidualBlock(8, 512, 1024)
        self.layer4 = _ResidualBlock(4, 1024, 1024, downsample=False)

    def forward(self, x):
        self.route = []
        x = self.conv3_1(x)
        x = self.conv3_2(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer8_1(x)
        self.route.append(self.layer8_1.route)  # route_1
        x = self.layer8_2(x)
        self.route.append(self.layer8_2.route)  # route_2
        x = self.layer4(x)
        return x

class Darknet53Clf(nn.Module):
    def __init__(self, num_classes=1000):
        super(Darknet53Clf, self).__init__()
        self.backbone = Darknet53()
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(1024, num_classes)

    def forward(self, x):
        x = self.backbone(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x

if __name__ == '__main__':
    from torchsummary import summary
    model = Darknet53Clf(20)
    summary(model.cuda(), (3, 416, 416), 2)


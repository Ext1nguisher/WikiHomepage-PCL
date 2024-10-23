import datetime
import hashlib
import re
import time
import struct

import requests
from bs4 import BeautifulSoup

response = requests.get("https://zh.minecraft.wiki").text
obj = BeautifulSoup(response, 'html.parser')


def while_delete(del_txts, txt, replacement=''):
    for del_txt in del_txts:
        while del_txt in txt:
            txt = txt.replace(del_txt, replacement)
    return txt


def get_news_card():
    resp = str(requests.get("https://news.bugjump.net/apis/versions/latest-card").text)
    return resp


def gr():
    origin = obj.find('div', class_="weekly-content").text
    result = origin.strip().split("。")
    result = [i.strip("\n") for i in result]
    result = [f"<ListItem><Paragraph>{i}。</Paragraph></ListItem>" for i in result]
    links = get_link_txt(str(obj.find('div', class_="weekly-content")))
    for k, v in links.items():
        result = [i.replace(k, link_to_xaml((k, v))) if k in i else i for i in result]
    result.pop()
    result[-1] = while_delete((' Margin="0,0,0,-8"',), result[-1])
    return result


def get_link_txt(txt):
    raw_links = re.findall(r'<a href=".*?" title=".*?"', txt, re.S)
    links = {}
    for link in raw_links:
        key = re.findall(r'title="(.*?)"', link, re.M)[0]
        ref = re.findall(r'href="(.*?)"', link, re.M)[0]
        links[key] = "https://zh.minecraft.wiki" + ref
    return links


def link_to_xaml(lk):
    xaml = f'''<Underline><local:MyTextButton EventType="打开网页" \
EventData="{lk[1]}" Margin="0,0,0,-8">{lk[0]}</local:MyTextButton></Underline>'''
    return xaml


def gs():
    img_src = 'https://zh.minecraft.wiki' + obj.find('div', class_='weekly-image').find('img')['src']
    img_src = re.sub(r'&', '&amp;', img_src)
    return img_src


def get_version():
    dt = datetime.datetime.now().strftime("%y%m%d")
    hsh = hashlib.md5(struct.pack('<f', time.time())).hexdigest()
    vid = f"{dt}:{hsh[:7]}"
    with open("Custom.xaml.ini", 'w') as f:
        f.write(f"{dt}:{hsh}")
    return vid


def update():
    now = datetime.datetime.now()
    content_text = '''<StackPanel Margin="0,-10,0,0"
xmlns:sys="clr-namespace:System;assembly=mscorlib"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
xmlns:local="clr-namespace:PCL;assembly=Plain Craft Launcher 2">
<!--Animations Starts-->
<StackPanel.Triggers>

</StackPanel.Triggers>
<StackPanel.Resources>
<!--Styles Starts-->
<Style TargetType="FlowDocumentScrollViewer" >
<Setter Property="IsSelectionEnabled" Value="False"/>
<Setter Property="VerticalScrollBarVisibility" Value="Hidden"/>
<Setter Property="Margin" Value="0"/>
</Style><Style TargetType="FlowDocument" >
<Setter Property="FontFamily" Value="Microsoft YaHei UI"/>
<Setter Property="FontSize" Value="14"/>
<Setter Property="TextAlignment" Value="Left"/>
</Style><Style TargetType="StackPanel" x:Key="ContentStack" >
<Setter Property="Margin" Value="20,40,20,20"/>
</Style><Style TargetType="local:MyCard" x:Key="Card" >
<Setter Property="Margin" Value="0,5"/>
</Style><Style TargetType="TextBox" x:Key="InlineCode">
    <Setter Property="FontSize" Value="14" />
    <Setter Property="IsReadOnly" Value="True" />
    <Setter Property="Margin" Value="2,0,2,-4" />
    <Setter Property="FontFamily" Value="Consolas"/>
    <Setter Property="Height" Value="18"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="TextBox">
                <Border Background="{DynamicResource ColorBrush6}" Opacity="0.9"
                    BorderBrush="{DynamicResource ColorBrush4}" BorderThickness="0"
                    CornerRadius="5" Padding="4,0.2">
                    <ScrollViewer x:Name="PART_ContentHost" Focusable="false"
                        HorizontalScrollBarVisibility="Hidden" VerticalScrollBarVisibility="Hidden" />
                </Border>
                <ControlTemplate.Triggers>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
<Style TargetType="Image" x:Key="InnerImage" >
<Setter Property="MaxHeight" Value="500"/>
<Setter Property="HorizontalAlignment" Value="Center"/>
</Style>
<Style TargetType="TextBlock" >
<Setter Property="TextWrapping" Value="Wrap"/>
<Setter Property="HorizontalAlignment" Value="Left"/>
<Setter Property="FontSize" Value="14"/>
<Setter Property="Foreground" Value="Black"/>
</Style>
<Style TargetType="List" >
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
<Setter Property="Margin" Value="20,0,0,0"/>
<Setter Property="MarkerStyle" Value="1"/>
<Setter Property="Padding" Value="0"/>
</Style>
<Style TargetType="ListItem" >
<Setter Property="Foreground" Value="Black"/>
<Setter Property="LineHeight" Value="22"/>
</Style
><Style TargetType="Paragraph" x:Key="H1" >
<Setter Property="FontSize" Value="24"/>
<Setter Property="Margin" Value="0,10,0,10"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H2" >
<Setter Property="FontSize" Value="22"/>
<Setter Property="Margin" Value="0,10,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
</Style>
<Style TargetType="local:MyTextButton" x:Key="TextButtonH2" >
<Setter Property="FontSize" Value="22"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H3" >
<Setter Property="FontSize" Value="18"/>
<Setter Property="Margin" Value="0,5,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H4" >
<Setter Property="FontSize" Value="16"/>
<Setter Property="Margin" Value="0,3,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H5" >
<Setter Property="FontSize" Value="15"/>
<Setter Property="Margin" Value="0,3,0,5"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
</Style>
<Style TargetType="Border" x:Key="Quote" >
<Setter Property="BorderThickness" Value="5,0,0,0"/>
<Setter Property="BorderBrush" Value="{DynamicResource ColorBrush4}"/>
<Setter Property="Padding" Value="10,5"/>
<Setter Property="Margin" Value="0,5"/>
</Style>
<Style x:Key="imgTitle" TargetType="TextBlock">
  <Setter Property="FontSize" Value="14" />
  <Setter Property="Foreground" Value="#FF777777" />
  <Setter Property="HorizontalAlignment" Value="Center" />
  <Setter Property="Margin" Value="0,0,0,15" />
</Style>
<sys:String x:Key="WikiIcon">
M172.61,196.65h31a7.69,7.69,0,0,1,7.62,6.65l11.19,80.95c2.58,20.09,5.16,40.18,7.73,60.79h1c3.61-20.61,7.47-41,11.34-60.79l18.23-81.58a7.7,7.7,0,0,1,7.52-6h26.58a7.7,7.7,0,0,1,7.51,6l18.48,81.6c3.86,19.57,7.21,40.18,11.07,60.79h1.29c2.32-20.61,4.9-41,7.22-60.79l11.67-81a7.7,7.7,0,0,1,7.62-6.6h27.72a7.7,7.7,0,0,1,7.59,9L364.41,382.2a7.69,7.69,0,0,1-7.58,6.38H311.61a7.7,7.7,0,0,1-7.54-6.14l-16-77.33c-3.09-14.68-5.67-30.14-7.47-44.57h-1c-2.58,14.43-4.9,29.89-7.73,44.57L256.34,382.4a7.7,7.7,0,0,1-7.54,6.18H204.6a7.69,7.69,0,0,1-7.58-6.32L165,205.72A7.71,7.71,0,0,1,172.61,196.65ZM286.87,507.39,159.71,455.25v22.82L97.54,451.18v-23.3l-89-2,9.54-119.29H44.78V291.24L31.45,280.81V247l14.09-4.23L45,227.13,63.33,220V207.1l5.51-2v-16.2l15.65-4.93V167.63l24.06-11.81,1.65-21.95,4.94-1.72-2-1V95.6h13V89.45l27.56-14.79L169,84.43,185.79,76l21.47,15.34,8.1,1v7.91h6.51l60.65-30.56,8,3.49,17-12.08L324,71l.12-2.19,39.15-22,18.06,12.53h26.37l3.79-1.62,36.38,27.4v28.77l16.81,8.15V149l6.08,3V164l10.15,5.51v11.32h9v11.52l1,0c1.54,0,3.44.08,5.91,0l15.13-.13V212.7h9.28v49.71h-5.8v36.1l-16,9h56l6.78,119.85-116.84-1.4Zm-157.16-85.7h27.23l128.51,52.7,152.82-78.54,92.15,1.1-3.36-59.47H456.67V325.89h-5.8v-40l22.37,1.81L485.36,281v-.86h-7.24V268.5h-7V236.33l-11.31,8.61V210.82h-9V187.35l-10.15-5.51V170.59l-11.59-5.79V138.2l-38.25-18.53,26.95-17.27v-2.29l-10.59-8-24.49,10.41V89.37H371.9l-10.35-7.18-8.38,4.7-.6,11.32-22.31,11.61-21.4-12.9L294,107.45l-10.58-4.63L192,148.87V130.24h-6.67V119l-1-.12V121l-28.12,4v.58h-7.1L151.49,150l-5.17-.37.11,3.38-1.27.44,14.7,10.59-45.37,22.26V206l-15.65,4.93V226l-5.51,2v12.57l-17.6,6.81.61,17.43-12,3.61,10.46,8.18v1.59h11.6v24l43.44,34.42h-84l-4.8,60,86.54,1.93v32.93l2.17.94ZM476.3,232.41h5.58v-4.25Z
</sys:String>
<sys:String x:Key="WikiPage">%(WikiPage)s</sys:String>
<Style TargetType="Border" x:Key="HeadImageBorder" >
<Setter Property="HorizontalAlignment" Value="Center"/>
<Setter Property="BorderThickness" Value="4"/>
<Setter Property="VerticalAlignment" Value="Top"/>
<Setter Property="BorderBrush" Value="{DynamicResource ColorBrush3}"/>
<Setter Property="CornerRadius" Value="7"/>
<Setter Property="MaxHeight" Value="140"/>
</Style><Style TargetType="Border" x:Key="TitleBorder" >
<Setter Property="Margin" Value="0,-20,-1,10"/>
<Setter Property="Background" Value="{DynamicResource ColorBrush3}"/>
<Setter Property="Width" Value="170"/>
<Setter Property="Height" Value="30"/>
<Setter Property="CornerRadius" Value="7"/>
<Setter Property="BorderThickness" Value="0,0,0,2"/>
<Setter Property="BorderBrush" Value="{DynamicResource ColorBrush2}"/>
</Style><Style TargetType="TextBlock" x:Key="TitleBlock" >
<Setter Property="HorizontalAlignment" Value="Center"/>
<Setter Property="TextAlignment" Value="Center"/>
<Setter Property="VerticalAlignment" Value="Center"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush7}"/>
<Setter Property="Width" Value="180"/>
<Setter Property="TextWrapping" Value="Wrap"/>
<Setter Property="FontSize" Value="18"/>
</Style>
</StackPanel.Resources>
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,-2,0,6">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="{DynamicResource ColorBrush5}" CornerRadius="5" VerticalAlignment="Top" BorderBrush="{DynamicResource ColorBrush3}" Opacity="0.7">
    <Grid Margin="10,0,0,0">
        <TextBlock x:Name="NewsHint" FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#FF000000">
                欢迎使用 Minecraft Wiki 摘录主页
    </TextBlock>
        <TextBlock x:Name="Hint2" FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#00000000">
                欢迎使用 Minecraft Wiki 摘录主页
    </TextBlock>
    </Grid>
</Border>
</local:MyCard>
<local:MyCard Title="中文 Minecraft Wiki 摘录 - 本周页面" CanSwap="True" IsSwaped="false" Style="{StaticResource Card}" >
<StackPanel Style="{StaticResource ContentStack}">
<Border Style="{StaticResource HeadImageBorder}">
<Border.Background>
<ImageBrush ImageSource="%(img)s" Stretch="UniformToFill" />
</Border.Background>
<Image Source="%(img)s" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{StaticResource TitleBorder}">
<TextBlock Style="{StaticResource TitleBlock}" Text="%(topic)s" />
</Border><FlowDocumentScrollViewer >
<FlowDocument>
<Paragraph Style="{StaticResource H2}">%(topic)s</Paragraph>
<List>
<!-- intro -->
%(intro)s
<!-- end_intro -->

</List><Paragraph Style="{StaticResource H3}">获取</Paragraph><List><!-- intro_2 -->
%(intro_2)s
<!-- end_intro_2 -->

</List><Paragraph Style="{StaticResource H3}">用途</Paragraph><List><!-- body -->
%(body)s
<!-- end_body -->
</List>
%(alt)s
</FlowDocument>
</FlowDocumentScrollViewer>
<Grid VerticalAlignment="Center" Margin="6,10,0,0" HorizontalAlignment="Right">
<Grid.ColumnDefinitions >
<ColumnDefinition Width="45"/>
<ColumnDefinition />
</Grid.ColumnDefinitions>
<Path Grid.Column="0" Margin="8,0" Height="28" Fill="{DynamicResource ColorBrush4}"
                    Stretch="Uniform"
                    Data="M4 2H2v12h2V4h10V2zm2 4h12v2H8v10H6zm4 4h12v12H10zm10 10v-8h-8v8z"/>
<TextBlock HorizontalAlignment="Right" Grid.Column="1" Text="仿生猫梦见苦力怕" FontSize="14" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}"/>
</Grid>
<TextBlock Margin="0,2" Grid.Column="1" HorizontalAlignment="Right" Text="%(datetime)s" FontSize="12" Foreground="{DynamicResource ColorBrush4}"/>
<local:MyIconTextButton Text="WIKI" ToolTip="在 Minecraft Wiki 上查看该页面" EventType="打开网页"
    EventData="{StaticResource WikiPage}" LogoScale="1.05" Logo="{StaticResource WikiIcon}" HorizontalAlignment="Left"/>
</StackPanel>
</local:MyCard>
<!-- NewsCard -->
%(NewsCard)s
<!-- end_NewsCard -->
<local:MyCard Margin="0,10,0,14">
<Border BorderBrush="{DynamicResource ColorBrush2}" Margin="-0.6" CornerRadius="5" BorderThickness="0,0,0,10">
<StackPanel>
  <Grid Margin="26,20,20,2">
    <StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="0,0,0,4">
    <TextBlock FontSize="18" Foreground="{DynamicResource ColorBrush2}"><Bold>PCL2 Wiki 摘录主页</Bold></TextBlock>
    <local:MyIconTextButton ColorType="Highlight" Margin="4,0" Text="%(version)s" ToolTip="当前版本号(非git)" 
    LogoScale="1.1" Logo="M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z" />
    </StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="-4,0,0,10" Height="56">
    <Image Margin="2" Source="http://creeperisaspy.tttttttttt.top/CardExt1nguisher.png"/>
    <TextBlock Margin="0,2" Grid.Column="1" HorizontalAlignment="Left" FontSize="12" Foreground="{DynamicResource ColorBrush4}">主页使用了来自<Underline><local:MyTextButton EventType="打开网页" EventData="https://github.com/Light-Beacon" Foreground="{DynamicResource ColorBrush4}">@最亮的信标</local:MyTextButton></Underline>的模板。</TextBlock>
    </StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="-8,0,0,10">
    <local:MyIconTextButton HorizontalAlignment="Left" Text="Gitee" ToolTip="前往Wiki 摘录主页 Gitee 页面" EventType="打开网页"
    EventData="https://gitee.com/planet_of_daniel/pcl2-homepage-fhg"
    LogoScale="1" Logo="M512 42.666667A464.64 464.64 0 0 0 42.666667 502.186667 460.373333 460.373333 0 0 0 363.52 938.666667c23.466667 4.266667 32-9.813333 32-22.186667v-78.08c-130.56 27.733333-158.293333-61.44-158.293333-61.44a122.026667 122.026667 0 0 0-52.053334-67.413333c-42.666667-28.16 3.413333-27.733333 3.413334-27.733334a98.56 98.56 0 0 1 71.68 47.36 101.12 101.12 0 0 0 136.533333 37.973334 99.413333 99.413333 0 0 1 29.866667-61.44c-104.106667-11.52-213.333333-50.773333-213.333334-226.986667a177.066667 177.066667 0 0 1 47.36-124.16 161.28 161.28 0 0 1 4.693334-121.173333s39.68-12.373333 128 46.933333a455.68 455.68 0 0 1 234.666666 0c89.6-59.306667 128-46.933333 128-46.933333a161.28 161.28 0 0 1 4.693334 121.173333A177.066667 177.066667 0 0 1 810.666667 477.866667c0 176.64-110.08 215.466667-213.333334 226.986666a106.666667 106.666667 0 0 1 32 85.333334v125.866666c0 14.933333 8.533333 26.88 32 22.186667A460.8 460.8 0 0 0 981.333333 502.186667 464.64 464.64 0 0 0 512 42.666667"/>
    <local:MyIconTextButton Text="CC BY-NC-SA 4.0" ToolTip="无特殊声明本主页文字内容使用该授权协议" EventType="打开网页"
    EventData="https://creativecommons.org/licenses/by-nc-sa/4.0/"
    LogoScale="1" Logo="M8.75.75V2h.985c.304 0 .603.08.867.231l1.29.736c.038.022.08.033.124.033h2.234a.75.75 0 0 1 0 1.5h-.427l2.111 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.006.005-.01.01-.045.04c-.21.176-.441.327-.686.45C14.556 10.78 13.88 11 13 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L12.178 4.5h-.162c-.305 0-.604-.079-.868-.231l-1.29-.736a.245.245 0 0 0-.124-.033H8.75V13h2.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.5V3.5h-.984a.245.245 0 0 0-.124.033l-1.289.737c-.265.15-.564.23-.869.23h-.162l2.112 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.016.015-.045.04c-.21.176-.441.327-.686.45C4.556 10.78 3.88 11 3 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L2.178 4.5H1.75a.75.75 0 0 1 0-1.5h2.234a.249.249 0 0 0 .125-.033l1.288-.737c.265-.15.564-.23.869-.23h.984V.75a.75.75 0 0 1 1.5 0Zm2.945 8.477c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L13 6.327Zm-10 0c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L3 6.327Z" />
    </StackPanel>
    </StackPanel>
    <StackPanel HorizontalAlignment="Right" >
    <local:MyIconTextButton HorizontalAlignment="Left" Text="反馈" ToolTip="反馈Wiki 摘录主页问题" EventType="打开网页"
    EventData="https://github.com/Ext1nguisher/PCLhomepage/issues/new"
    LogoScale="1" Logo="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0z M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0z"/>
    <local:MyIconTextButton HorizontalAlignment="Left" Text="刷新" ToolTip="刷新Wiki 摘录主页主页" EventType="刷新主页"
    LogoScale="0.9" Logo="M960 416V192l-73.056 73.056a447.712 447.712 0 0 0-373.6-201.088C265.92 63.968 65.312 264.544 65.312 512S265.92 960.032 513.344 960.032a448.064 448.064 0 0 0 415.232-279.488 38.368 38.368 0 1 0-71.136-28.896 371.36 371.36 0 0 1-344.096 231.584C308.32 883.232 142.112 717.024 142.112 512S308.32 140.768 513.344 140.768c132.448 0 251.936 70.08 318.016 179.84L736 416h224z"/>
    </StackPanel>
  </Grid>
  </StackPanel>
</Border>
</local:MyCard>
</StackPanel>'''
    with open("Custom.xaml", "w", encoding='UTF-8') as f:
        f.write(content_text % {
            'datetime': f'最后更新: {now.strftime("%Y-%m-%d")}',
            'WikiPage': list(get_link_txt(str(obj.find('div', class_="weekly-content"))).values())[0],
            'topic': list(get_link_txt(str(obj.find('div', class_="weekly-content"))).keys())[0],
            'intro': gr()[0],
            'intro_2': gr()[1],
            'body': '\n'.join(gr()[2:-1]),
            'alt': gr()[-1].replace("<ListItem>", '').replace("</ListItem>", ''),
            'img': gs(),
            'NewsCard': get_news_card(),
            'version': get_version()
        })


update()

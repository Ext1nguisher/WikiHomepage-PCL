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


def get_img_alt():
    return gr()[-1].replace("<ListItem>", '').replace("</ListItem>", '')


def get_wiki_page():
    return list(get_link_txt(str(obj.find('div', class_="weekly-content"))).values())[0]


def get_topic():
    return list(get_link_txt(str(obj.find('div', class_="weekly-content"))).keys())[0]


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
<Style x:Key="TabControlStyle" TargetType="{x:Type TabControl}">
    <Setter Property="Padding" Value="2"/>
    <Setter Property="HorizontalContentAlignment" Value="Center"/>
    <Setter Property="VerticalContentAlignment" Value="Center"/>
    <Setter Property="Background" Value="Transparent"/>
    <Setter Property="BorderBrush" Value="#FFACACAC"/>
    <Setter Property="BorderThickness" Value="0"/>
    <Setter Property="Foreground" Value="{DynamicResource {x:Static SystemColors.ControlTextBrushKey}}"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type TabControl}">
                    <Grid x:Name="templateRoot" ClipToBounds="True" SnapsToDevicePixels="True" KeyboardNavigation.TabNavigation="Local">
                        <Grid.ColumnDefinitions>
                            <ColumnDefinition x:Name="ColumnDefinition0"/>
                            <ColumnDefinition x:Name="ColumnDefinition1" Width="0"/>
                        </Grid.ColumnDefinitions>
                        <Grid.RowDefinitions>
                            <RowDefinition x:Name="RowDefinition0" Height="Auto"/>
                            <RowDefinition x:Name="RowDefinition1" Height="*"/>
                        </Grid.RowDefinitions>
                    <UniformGrid x:Name="HeaderPanel" Rows="1" Background="Transparent" Grid.Column="0" IsItemsHost="True" Margin="0" Grid.Row="0" KeyboardNavigation.TabIndex="1" Panel.ZIndex="1"/>
                    <Line X1="0" X2="{Binding ActualWidth, RelativeSource={RelativeSource Self}}" Stroke="White" StrokeThickness="0.1" VerticalAlignment="Bottom" Margin="0 0 0 1" SnapsToDevicePixels="True"/>
                    <Border x:Name="ContentPanel" BorderBrush="{DynamicResource ColorBrush2}" BorderThickness="0" Background="Transparent" Grid.Column="0" KeyboardNavigation.DirectionalNavigation="Contained" Grid.Row="1" KeyboardNavigation.TabIndex="2" KeyboardNavigation.TabNavigation="Local" CornerRadius="7">
                        <ContentPresenter x:Name="PART_SelectedContentHost" ContentTemplate="{TemplateBinding SelectedContentTemplate}" Content="{TemplateBinding SelectedContent}" ContentStringFormat="{TemplateBinding SelectedContentStringFormat}" ContentSource="SelectedContent" Margin="0" SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}"/>
                    </Border>
                </Grid>
                <ControlTemplate.Triggers>
                    <Trigger Property="TabStripPlacement" Value="Bottom">
                        <Setter Property="Grid.Row" TargetName="HeaderPanel" Value="1"/>
                        <Setter Property="Grid.Row" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Height" TargetName="RowDefinition0" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition1" Value="Auto"/>
                    </Trigger>
                    <Trigger Property="TabStripPlacement" Value="Left">
                        <Setter Property="Grid.Row" TargetName="HeaderPanel" Value="0"/>
                        <Setter Property="Grid.Row" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Grid.Column" TargetName="HeaderPanel" Value="0"/>
                        <Setter Property="Grid.Column" TargetName="ContentPanel" Value="1"/>
                        <Setter Property="Width" TargetName="ColumnDefinition0" Value="Auto"/>
                        <Setter Property="Width" TargetName="ColumnDefinition1" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition0" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition1" Value="0"/>
                    </Trigger>
                    <Trigger Property="TabStripPlacement" Value="Right">
                        <Setter Property="Grid.Row" TargetName="HeaderPanel" Value="0"/>
                        <Setter Property="Grid.Row" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Grid.Column" TargetName="HeaderPanel" Value="1"/>
                        <Setter Property="Grid.Column" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Width" TargetName="ColumnDefinition0" Value="*"/>
                        <Setter Property="Width" TargetName="ColumnDefinition1" Value="Auto"/>
                        <Setter Property="Height" TargetName="RowDefinition0" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition1" Value="0"/>
                    </Trigger>
                    <Trigger Property="IsEnabled" Value="False">
                        <Setter Property="TextElement.Foreground" TargetName="templateRoot" Value="{DynamicResource {x:Static SystemColors.GrayTextBrushKey}}"/>
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
<Style x:Key="TabItemStyle" TargetType="{x:Type TabItem}">
    <Setter Property="Foreground" Value="Black"/>
    <Setter Property="Background" Value="Transparent"/>
    <Setter Property="BorderBrush" Value="#fff"/>
    <Setter Property="Margin" Value="0,0,0,8"/>
    <Setter Property="HorizontalContentAlignment" Value="Stretch"/>
    <Setter Property="VerticalContentAlignment" Value="Stretch"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="{x:Type TabItem}">
                <Grid x:Name="templateRoot"  SnapsToDevicePixels="True" Background="Transparent">
                    <Grid.ColumnDefinitions>
                        <ColumnDefinition Width="*"/>
                    </Grid.ColumnDefinitions>
                    <Border x:Name="ContentPanel" BorderBrush="{DynamicResource ColorBrush2}" BorderThickness="0,0,0,2" Background="White" Grid.Column="0" KeyboardNavigation.DirectionalNavigation="Contained"
                        Grid.Row="0" KeyboardNavigation.TabIndex="2" KeyboardNavigation.TabNavigation="Local" CornerRadius="7" Height="30" Margin="2,0,2,0"/>
                    <TextBlock x:Name="txt" Visibility="Visible" VerticalAlignment="Center" HorizontalAlignment="Center"
                    Text="{TemplateBinding Header}" ToolTip="{TemplateBinding Header}" Foreground="{TemplateBinding Foreground}" TextTrimming="CharacterEllipsis"/>
                </Grid>
                <ControlTemplate.Triggers>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsMouseOver, RelativeSource={RelativeSource Self}}" Value="true"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Top"/>
                        </MultiDataTrigger.Conditions>

                        <Setter Property="Foreground" TargetName="txt" Value="Blue"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Left"/>
                        </MultiDataTrigger.Conditions>
                            <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Bottom"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Right"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Top"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>

                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsSelected, RelativeSource={RelativeSource Self}}" Value="true"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Top"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Panel.ZIndex" Value="1"/>
                        <Setter Property="Foreground" TargetName="txt" Value="Green"/>
                    </MultiDataTrigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
<Style TargetType="FlowDocumentScrollViewer">
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
</Style>
<Style TargetType="TextBox" x:Key="InlineCode">
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
<sys:String x:Key="TranslateIcon">
M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z
</sys:String>
<sys:String x:Key="CreeperIcon">
M213.333333 128a85.333333 85.333333 0 0 0-85.333333 85.333333v597.333334a85.333333 85.333333 0 0 0 85.333333 85.333333h597.333334a85.333333 85.333333 0 0 0 85.333333-85.333333V213.333333a85.333333 85.333333 0 0 0-85.333333-85.333333H213.333333z m0 64h597.333334c11.754667 0 21.333333 9.578667 21.333333 21.333333v597.333334c0 11.754667-9.578667 21.333333-21.333333 21.333333H213.333333c-11.754667 0-21.333333-9.578667-21.333333-21.333333V213.333333c0-11.754667 9.578667-21.333333 21.333333-21.333333z m64 106.666667a21.333333 21.333333 0 0 0-21.333333 21.333333v128a21.333333 21.333333 0 0 0 21.333333 21.333333h149.333334v-149.333333a21.333333 21.333333 0 0 0-21.333334-21.333333h-128z m149.333334 170.666666v85.333334h-64a21.333333 21.333333 0 0 0-21.333334 21.333333v160a32 32 0 1 0 64 0V704h213.333334v32a32 32 0 1 0 64 0V576a21.333333 21.333333 0 0 0-21.333334-21.333333h-64v-85.333334h-170.666666z m170.666666 0h149.333334a21.333333 21.333333 0 0 0 21.333333-21.333333v-128a21.333333 21.333333 0 0 0-21.333333-21.333333h-128a21.333333 21.333333 0 0 0-21.333334 21.333333v149.333333z
</sys:String>
<sys:String x:Key="thanks">
鸣谢|一些对主页开发有帮助的人: \n
土星仙鹤 @ QQ(2480379448) 主页初版的首个测试者! \n
ess的大清要活了 ~喵 @ QQ(1837750594) 带我接触了自定义主页,没有他我可能到现在还不知道主页是什么! \n
最亮的信标 @ Github(Nattiden) 提供主页模板,本主页使用他的NewsHomepage为基础开发! \n
Mfn233 @ Github(Mfn233) 为主页提供最开始的技术支持支持和鼓励 \n
主页群的各位 @ QQ群(828081791等) 为主页的开发提供持续的精神力量,快来一起咕咕咕! \n
凌云 @ Github(JingHai-Lingyun) 提供挂载主页的oss,真的真的非常感激! \n
排列没啥顺序，个个我都非常非常非常谢谢你们!
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
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,-2,0,5">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="{DynamicResource ColorBrush5}" CornerRadius="5" VerticalAlignment="Top" BorderBrush="{DynamicResource ColorBrush3}" Opacity="0.7">
    <Grid Margin="10,0,0,0">
        <TextBlock x:Name="NewsHint" FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#FF000000">
                🖼️ 欢迎使用杂志主页
    </TextBlock>
        <TextBlock x:Name="Hint2" FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#00000000">
                🖼️ 欢迎使用杂志主页
    </TextBlock>
    </Grid>
</Border>
</local:MyCard>
<TabControl Style="{StaticResource TabControlStyle}" FontFamily="Microsoft YaHei UI" FontSize="17">
    <TabItem Header="中文 Minecraft Wiki 摘录 - 本周页面" Style="{StaticResource TabItemStyle}">
<local:MyCard>
<StackPanel Style="{StaticResource ContentStack}">
<Border Style="{StaticResource HeadImageBorder}">
<Border.Background>
<ImageBrush ImageSource="https://zh.minecraft.wiki/images/thumb/Bedrock_1.21.50.28_PatchNotes.png/700px-Bedrock_1.21.50.28_PatchNotes.png??format=original" Stretch="UniformToFill" />
</Border.Background>
<Image Source="https://zh.minecraft.wiki/images/thumb/Bedrock_1.21.50.28_PatchNotes.png/700px-Bedrock_1.21.50.28_PatchNotes.png??format=original" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{StaticResource TitleBorder}">
<TextBlock Style="{StaticResource TitleBlock}" Text="苍白垂须" />
</Border><FlowDocumentScrollViewer >
<FlowDocument>
<Paragraph Style="{StaticResource H2}">苍白垂须</Paragraph>
<List>
<!-- intro -->
<ListItem><Paragraph><Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>是一种生成于苍白之园生物群系的方块。</Paragraph></ListItem>
<!-- end_intro -->

</List><Paragraph Style="{StaticResource H3}">合成 &amp; 生成</Paragraph><List><!-- intro_2 -->
<ListItem><Paragraph><Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>会自然生成于苍白之园生物群系中<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E6%A9%A1%E6%A0%91" Margin="0,0,0,-8">苍白橡树</local:MyTextButton></Underline>的树干和树叶下方。</Paragraph></ListItem>
<ListItem><Paragraph><Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>也可以通过与<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E6%B5%81%E6%B5%AA%E5%95%86%E4%BA%BA" Margin="0,0,0,-8">流浪商人</local:MyTextButton></Underline>交易获得。</Paragraph></ListItem>
<!-- end_intro_2 -->
</List>
<Paragraph Style="{StaticResource H3}">特性 &amp; 用途</Paragraph><List>
<ListItem><Paragraph>没有被<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E5%89%AA%E5%88%80" Margin="0,0,0,-8">剪刀</local:MyTextButton></Underline>或具有<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E7%B2%BE%E5%87%86%E9%87%87%E9%9B%86" Margin="0,0,0,-8">精准采集</local:MyTextButton></Underline>的工具挖掘破坏时，<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>被破坏后不会掉落。</Paragraph></ListItem>
<ListItem><Paragraph>当放置在苍白橡木原木、苍白橡木、去皮苍白橡木原木、去皮苍白橡木[仅<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/Java%E7%89%88" Margin="0,0,0,-8">Java版</local:MyTextButton></Underline>]或<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E6%A9%A1%E6%A0%91" Margin="0,0,0,-8">苍白橡树</local:MyTextButton></Underline>树叶下方时，<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>每<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E5%88%BB" Margin="0,0,0,-8">刻</local:MyTextButton></Underline>有1⁄500的概率发出特殊的环境音效。</Paragraph></ListItem>
<ListItem><Paragraph><Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>不会自然生长。</Paragraph></ListItem>
<ListItem><Paragraph>对<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB" Margin="0,0,0,-8">苍白垂须</local:MyTextButton></Underline>使用骨粉会使其向下生长一格。</Paragraph></ListItem>
</List>

<Paragraph>图为苍白之园中生成的<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E8%8B%8D%E7%99%BD%E5%9E%82%E9%A1%BB">苍白垂须</local:MyTextButton></Underline>。</Paragraph>
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
    </TabItem>
<TabItem Header="Minecraft官方博文 - 识海漫谈" Style="{StaticResource TabItemStyle}">
<local:MyCard>
<StackPanel Style="{StaticResource ContentStack}">
<Border Style="{StaticResource HeadImageBorder}">
<Border.Background>
<ImageBrush ImageSource="https://www.helloimg.com/i/2024/12/15/675ebe72302be.jpg" Stretch="UniformToFill" />
</Border.Background>
<Image Source="https://www.helloimg.com/i/2024/12/15/675ebe72302be.jpg" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{StaticResource TitleBorder}">
<TextBlock Style="{StaticResource TitleBlock}" Text="废弃矿井" />
</Border><FlowDocumentScrollViewer>
<FlowDocument>
<Paragraph Style="{StaticResource H2}">结构寻访：废弃矿井</Paragraph>
<Paragraph Style="{StaticResource H5}">昔人已乘黄鹤去，此地空余黄鹤楼。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">当你四处跑图时，每隔一段时间，你就会偶然发现先人的足迹。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">在你考古时发现的陶片，通向下界的废弃传送门，以及久已灭绝物种的巨大化石，无不揭示了你所探索世界的绵长历史。</Paragraph>
<Paragraph Margin="0,0" Foreground="black"><!-- 换行 --></Paragraph>
<Paragraph Margin="0,0" Foreground="black">但与这些看来时代久远的文物不同，其中的一些显得更为接近我们所生活的年代。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">这当中最好的例子便是废弃矿井——它会偶然在深洞中出现。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">它清楚地证明了先人尝试榨干主世界资源的企图，这可能就是钻石难以找到的原因吧！</Paragraph>
<BlockUIContainer>
<StackPanel>
<Image Style="{StaticResource InnerImage}" Source="https://www.helloimg.com/i/2024/12/15/675ebe6f7b24e.png"/>
<TextBlock Text="游戏中的废弃矿井" Style="{StaticResource imgTitle}" />
</StackPanel>
</BlockUIContainer>
<Paragraph Margin="0,0" Foreground="black">第一个废弃矿井的出现始于2011年6月的<Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki/w/%E5%86%92%E9%99%A9%E6%9B%B4%E6%96%B0" Margin="0">冒险更新</local:MyTextButton></Underline>。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">它易于辨认——主体为由3x3隧道构成的密集网络，布有橡木和铁轨，且穿插着大量的蜘蛛网。其在与峡谷相交时最容易被发现。</Paragraph>
<Paragraph Margin="0,0" Foreground="black"><!-- 换行 --></Paragraph>
<Paragraph Margin="0,0" Foreground="black">矿物资源和战利品使它们成为玩家们探索的好去处：</Paragraph>
<Paragraph Margin="0,0" Foreground="black">在废弃矿井的墙壁上，你会常常看见矿工们遗忘的矿物，这使得探索废弃矿井成为初期快速积攒铁锭、铜锭和金锭等基础资源的方法之一。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">但这还不是全部，那些神秘的矿工们还留下了许多满载着食物、火把、铁路设施和其他好东西的运输矿车。</Paragraph>
<Paragraph Margin="0,0" Foreground="black"><!-- 换行 --></Paragraph>
<Paragraph Margin="0,0" Foreground="black">但也请在探索时保持警惕，因为废弃矿井中的黑暗环境造就了一个怪物刷新的绝佳地点。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">不仅有一般的亡灵生物和苦力怕，你还会找到在废弃矿井中找到一种特殊的&quot;洞穴蜘蛛&quot;</Paragraph>
<Paragraph Margin="0,0" Foreground="black">这个体型更小的蜘蛛种群不仅更难以击中，还在攻击时造成负面的状态效果。千万要远离。</Paragraph>
<BlockUIContainer>
<StackPanel>
<Image Style="{StaticResource InnerImage}" Source="https://www.helloimg.com/i/2024/12/15/675ebe6faa984.png"/>
<TextBlock Text="现实中的矿巷 —— 图片版权协议: EwkaC // CC BY-SA 4.0" Style="{StaticResource imgTitle}" />
</StackPanel>
</BlockUIContainer>
<Paragraph Margin="0,0" Foreground="black">在真实世界中，人类已经为了获取资源而建造了数千年的矿井。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">最早的地下矿井仅仅像是经过人工扩张的自然洞穴。但罗马人大幅度改进了相关的工艺水准——他们开凿了通往矿井的运水槽，这样，他们不仅可以用水定位矿脉，还能清除矿渣和残骸。</Paragraph>
<Paragraph Margin="0,0" Foreground="black"><!-- 换行 --></Paragraph>
<Paragraph Margin="0,0" Foreground="black">在矿业术语中，“矿井”指将人和物带上地面的垂直隧道，通常使用某种升降机。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">而游戏中的横向隧道则叫做“矿巷”或“坑道”，就像在游戏中一样，它们通常由木结构支撑起来以减少发生坍塌事故的风险。</Paragraph>
<Paragraph Margin="0,0" Foreground="black"><!-- 换行 --></Paragraph>
<Paragraph Margin="0,0" Foreground="black">当今，你可能会以为采矿工业已经高度机器化并由机器人完成——在一些地方的确如此。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">但在大多数地方，采矿的工作仍依赖于人们在恶劣和危险的条件下辛勤工作的成果。</Paragraph>
<Paragraph Margin="0,0" Foreground="black">采矿对环境的负面影响也是一个日益严重的问题，有人担心生活所需的最重要的一些资源正因而逐渐枯竭。</Paragraph>
<Paragraph Margin="0,0" Foreground="black"><!-- 换行 --></Paragraph>
<Paragraph Margin="0,0" Foreground="black">在游戏中，供你游玩的世界是无限的——如果你在一个地方挖完了所有煤矿，你大可以直接换个地方继续挖。地球上？我们不可能再那样“奢侈”了……</Paragraph>
</FlowDocument>
</FlowDocumentScrollViewer>
<Grid VerticalAlignment="Center" Margin="6,10,0,0" HorizontalAlignment="Right">
<Grid.ColumnDefinitions >
<ColumnDefinition Width="45"/>
<ColumnDefinition />
</Grid.ColumnDefinitions>
<Path Grid.Column="0" Margin="8,0" Height="28" Fill="{DynamicResource ColorBrush4}"
                    Stretch="Uniform"
                    Data="M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z"/>
<TextBlock HorizontalAlignment="Right" Grid.Column="1" Text="仿生猫梦见苦力怕" FontSize="14" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}"/>
</Grid>
<TextBlock Margin="0,2" Grid.Column="1" HorizontalAlignment="Right" Text="最后更新: 2024-11-23" FontSize="12" Foreground="{DynamicResource ColorBrush4}"/>
<local:MyIconTextButton Text="访问原址" ToolTip="在 MC 官网上查看该页面" EventType="打开网页" Margin="0,0,0,12"
    EventData="https://www.minecraft.net/en-us/article/mineshaft" LogoScale="1.05" Logo="{StaticResource CreeperIcon}" HorizontalAlignment="Left"/>
<StackPanel Margin="16,0,23,20" VerticalAlignment="bottom">
    <Grid>
      <Grid.ColumnDefinitions>
        <ColumnDefinition Width="1*"/>
        <ColumnDefinition Width="120"/>
      </Grid.ColumnDefinitions>
      <local:MyComboBox x:Name="jumpbox" Height="30" SelectedIndex="0">
        <local:MyComboBoxItem Content="古迹废墟"/>
      </local:MyComboBox>
        <local:MyButton HorizontalAlignment="Center" Width="92"
            Grid.Column="1" Text="打开→" EventType="打开帮助"
            EventData="{Binding Path=Text,ElementName=jumpbox,StringFormat=http://pclhomeplazaoss.lingyunawa.top:26995/d/Homepages/Ext1nguisher/h{0}.json}"/>
    </Grid>
</StackPanel>
</StackPanel>
</local:MyCard>
</TabItem>
<TabItem Header="其他" Style="{StaticResource TabItemStyle}">
<!-- NewsCard -->
<local:MyCard Title="最新版本" CanSwap="False" IsSwaped="False" >
<StackPanel Margin="8,35,8,15">
<local:MyListItem Margin="10,1,10,1" ToolTip="最新正式版 点击查看该版本更新日志"
	Logo="pack://application:,,,/images/Blocks/Grass.png" Title="最新正式版 - 1.21.4" Info="正式版"
	EventType="打开帮助" EventData="https://news.bugjump.net/VersionDetail.json?ver=1.21.4" Type="Clickable" />
</StackPanel>
</local:MyCard>
<!-- end_NewsCard -->
</TabItem>
</TabControl>
<local:MyCard Margin="0,10,0,14">
<Border BorderBrush="{DynamicResource ColorBrush2}" Margin="-0.6" CornerRadius="5" BorderThickness="0,0,0,10">
<StackPanel>
  <Grid Margin="26,20,20,2">
    <StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="0,0,0,4">
    <TextBlock FontSize="18" Foreground="{DynamicResource ColorBrush2}"><Bold>PCL2 杂志主页</Bold></TextBlock>
    <local:MyIconTextButton ColorType="Highlight" Margin="4,0" Text="250106:eb03ad9" ToolTip="当前版本号(非git)"
    LogoScale="1.1" Logo="M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z" />
    </StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="0,0,0,10">
    <TextBlock HorizontalAlignment="Left" Grid.Column="0" FontSize="13" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}">
        <Run>主页制作: 仿生猫梦见苦力怕 / CreeperIsASpy</Run>
        <LineBreak/>
        <Run>更新时间: 周一下午到周二下午（本人初中生学业紧张理解一下）</Run>
        <LineBreak/>
        <Run>内容取自</Run><Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki">中文 Minecraft Wiki</local:MyTextButton></Underline>
        <Run>中“本周页面”板块以及 </Run><Underline><local:MyTextButton EventType="打开网页" EventData="https://minecraft.net">MC 官网</local:MyTextButton></Underline>。
    </TextBlock>
    </StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="-8,0,0,10">
    <local:MyIconTextButton HorizontalAlignment="Left" Text="Gitee" ToolTip="前往杂志主页 Gitee 页面" EventType="打开网页"
    EventData="https://gitee.com/planet_of_daniel/pcl2-homepage-fhg"
    LogoScale="1" Logo="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12a12 12 0 0 0 12-12A12 12 0 0 0 12 0zm6.09 5.333c.328 0 .593.266.592.593v1.482a.594.594 0 0 1-.593.592H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h5.63c.982 0 1.778-.796 1.778-1.778v-.296a.593.593 0 0 0-.592-.593h-4.15a.59.59 0 0 1-.592-.592v-1.482a.593.593 0 0 1 .593-.592h6.815c.327 0 .593.265.593.592v3.408a4 4 0 0 1-4 4H5.926a.593.593 0 0 1-.593-.593V9.778a4.444 4.444 0 0 1 4.445-4.444h8.296Z"/>
    <local:MyIconTextButton Text="CC BY-NC-SA 4.0" ToolTip="无特殊声明本主页文字内容使用该授权协议" EventType="打开网页"
    EventData="https://creativecommons.org/licenses/by-nc-sa/4.0/"
    LogoScale="1" Logo="M8.75.75V2h.985c.304 0 .603.08.867.231l1.29.736c.038.022.08.033.124.033h2.234a.75.75 0 0 1 0 1.5h-.427l2.111 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.006.005-.01.01-.045.04c-.21.176-.441.327-.686.45C14.556 10.78 13.88 11 13 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L12.178 4.5h-.162c-.305 0-.604-.079-.868-.231l-1.29-.736a.245.245 0 0 0-.124-.033H8.75V13h2.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.5V3.5h-.984a.245.245 0 0 0-.124.033l-1.289.737c-.265.15-.564.23-.869.23h-.162l2.112 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.016.015-.045.04c-.21.176-.441.327-.686.45C4.556 10.78 3.88 11 3 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L2.178 4.5H1.75a.75.75 0 0 1 0-1.5h2.234a.249.249 0 0 0 .125-.033l1.288-.737c.265-.15.564-.23.869-.23h.984V.75a.75.75 0 0 1 1.5 0Zm2.945 8.477c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L13 6.327Zm-10 0c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L3 6.327Z" />
    </StackPanel>
    </StackPanel>
    <StackPanel HorizontalAlignment="Right" >
    <local:MyIconTextButton HorizontalAlignment="Left" Text="反馈" ToolTip="反馈主页问题" EventType="打开网页"
    EventData="https://gitee.com/planet_of_daniel/pcl2-homepage-fhg/issues/new"
    LogoScale="1" Logo="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0z M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0z"/>
    <local:MyIconTextButton HorizontalAlignment="Left" Text="刷新" ToolTip="刷新主页" EventType="刷新主页"
    LogoScale="0.9" Logo="M960 416V192l-73.056 73.056a447.712 447.712 0 0 0-373.6-201.088C265.92 63.968 65.312 264.544 65.312 512S265.92 960.032 513.344 960.032a448.064 448.064 0 0 0 415.232-279.488 38.368 38.368 0 1 0-71.136-28.896 371.36 371.36 0 0 1-344.096 231.584C308.32 883.232 142.112 717.024 142.112 512S308.32 140.768 513.344 140.768c132.448 0 251.936 70.08 318.016 179.84L736 416h224z"/>
    <local:MyIconTextButton HorizontalAlignment="Left" Text="鸣谢" ToolTip="鸣谢人员名单及其联系方式" EventType="弹出窗口" EventData="{StaticResource thanks}"
    LogoScale="0.9" Logo="M6.26 21.388H6c-.943 0-1.414 0-1.707-.293C4 20.804 4 20.332 4 19.389v-1.112c0-.518 0-.777.133-1.009s.334-.348.736-.582c2.646-1.539 6.403-2.405 8.91-.91q.253.151.45.368a1.49 1.49 0 0 1-.126 2.134a1 1 0 0 1-.427.24q.18-.021.345-.047c.911-.145 1.676-.633 2.376-1.162l1.808-1.365a1.89 1.89 0 0 1 2.22 0c.573.433.749 1.146.386 1.728c-.423.678-1.019 1.545-1.591 2.075s-1.426 1.004-2.122 1.34c-.772.373-1.624.587-2.491.728c-1.758.284-3.59.24-5.33-.118a15 15 0 0 0-3.017-.308m4.601-18.026C11.368 2.454 11.621 2 12 2s.632.454 1.139 1.363l.13.235c.145.259.217.388.329.473s.252.117.532.18l.254.058c.984.222 1.476.334 1.593.71s-.218.769-.889 1.553l-.174.203c-.19.223-.285.334-.328.472s-.029.287 0 .584l.026.27c.102 1.047.152 1.57-.154 1.803s-.767.02-1.688-.404l-.239-.11c-.261-.12-.392-.18-.531-.18s-.27.06-.531.18l-.239.11c-.92.425-1.382.637-1.688.404s-.256-.756-.154-1.802l.026-.271c.029-.297.043-.446 0-.584s-.138-.25-.328-.472l-.174-.203c-.67-.784-1.006-1.177-.889-1.553s.609-.488 1.593-.71l.254-.058c.28-.063.42-.095.532-.18s.184-.214.328-.473zm8.569 4.319c.254-.455.38-.682.57-.682s.316.227.57.682l.065.117c.072.13.108.194.164.237s.126.058.266.09l.127.028c.492.112.738.167.796.356s-.109.384-.444.776l-.087.101c-.095.112-.143.168-.164.237s-.014.143 0 .292l.013.135c.05.523.076.785-.077.901s-.383.01-.844-.202l-.12-.055c-.13-.06-.196-.09-.265-.09c-.07 0-.135.03-.266.09l-.119.055c-.46.212-.69.318-.844.202c-.153-.116-.128-.378-.077-.901l.013-.135c.014-.15.022-.224 0-.292c-.021-.07-.069-.125-.164-.237l-.087-.101c-.335-.392-.503-.588-.444-.776s.304-.244.796-.356l.127-.028c.14-.032.21-.048.266-.09c.056-.043.092-.108.164-.237zm-16 0C3.685 7.227 3.81 7 4 7s.316.227.57.682l.065.117c.072.13.108.194.164.237s.126.058.266.09l.127.028c.492.112.738.167.797.356c.058.188-.11.384-.445.776l-.087.101c-.095.112-.143.168-.164.237s-.014.143 0 .292l.013.135c.05.523.076.785-.077.901s-.384.01-.844-.202l-.12-.055c-.13-.06-.196-.09-.265-.09c-.07 0-.135.03-.266.09l-.119.055c-.46.212-.69.318-.844.202c-.153-.116-.128-.378-.077-.901l.013-.135c.014-.15.022-.224 0-.292c-.021-.07-.069-.125-.164-.237l-.087-.101c-.335-.392-.503-.588-.445-.776c.059-.189.305-.244.797-.356l.127-.028c.14-.032.21-.048.266-.09c.056-.043.092-.108.164-.237z"/>
    </StackPanel>
  </Grid>
</StackPanel>
</Border>
</local:MyCard>
</StackPanel>'''
    with open("Custom.xaml", "w", encoding='UTF-8') as f:
        f.write(content_text % {
            'datetime': f'最后更新: {now.strftime("%Y-%m-%d")}',
            'WikiPage': get_wiki_page(),
            'topic': get_topic(),
            'intro': gr()[0],                       # 内容的第一句
            'intro_2': gr()[1],                     # 内容的第二句
            'body': '\n'.join(gr()[2:-1]),          # 内容剩余部分
            'alt': get_img_alt(),
            'img': gs(),
            'NewsCard': get_news_card(),
            'version': get_version()
        })


def print_out():
    print(f'INTRO $1:\n\t{gr()[0]}\n')
    print(f'INTRO $2:\n\t{gr()[1]}\n')
    BODYTXT = '\n'.join(gr()[2:-1])
    print(f'BODY:    \n{BODYTXT}\n')
    ALTTXT = gr()[-1].replace("<ListItem>", '').replace("</ListItem>", '')
    print(f'ALT:\n\t{ALTTXT}\n')
    print(f'IMG: \n\t{gs()}\n')
    print(f'$NEWSCARD:     \n{get_news_card()}\n')
    print(f'$VID:     {get_version()}')


print_out()

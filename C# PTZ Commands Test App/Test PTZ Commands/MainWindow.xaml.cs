using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Test_PTZ_Commands
{
    /// <summary>
    /// Logica di interazione per MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        Socket client;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void clickRight(object sender, RoutedEventArgs e)
        {
            sendMessage(Messages.Right);
        }

        private void clickLeft(object sender, RoutedEventArgs e)
        {
            sendMessage(Messages.Left);
        }

        private void click_connect(object sender, RoutedEventArgs e)
        {
            try
            {
                IPAddress ipAddress = IPAddress.Parse(tb_ipaddress.Text);
                this.client = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
                int port = Int32.Parse(tb_port.Text);
                client.Connect(ipAddress, port);
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void click_disconnect(object sender, RoutedEventArgs e)
        {
            try {
                if (client!= null && client.Connected)
                {
                    client.Disconnect(false);
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void clickUp(object sender, RoutedEventArgs e)
        {
            sendMessage(Messages.Up);
        }

        private void clickDown(object sender, RoutedEventArgs e)
        {
            sendMessage(Messages.Down);
        }


        private void sendMessage (byte[] message)
        {
            try
            {
                    client.Send(message);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}

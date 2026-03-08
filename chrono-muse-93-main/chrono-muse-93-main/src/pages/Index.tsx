import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import ChatWindow from "@/components/ChatWindow";
import { PanelLeft } from "lucide-react";

const Index = () => (
  <SidebarProvider>
    <div className="min-h-screen flex w-full">
      <AppSidebar />
      <div className="flex-1 flex flex-col relative">
        <header className="absolute top-0 left-0 z-20 p-2">
          <SidebarTrigger className="text-muted-foreground hover:text-foreground" />
        </header>
        <ChatWindow />
      </div>
    </div>
  </SidebarProvider>
);

export default Index;

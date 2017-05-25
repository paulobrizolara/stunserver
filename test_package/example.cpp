
#define NDEBUG

#include "stuntman/commonincludes.hpp"
#include "stuntman/stuncore.h"
#include "stuntman/server.h"

#include <iostream>

HRESULT StartUDP(CRefCountedPtr<CStunServer>& spServer, CStunServerConfig& config)
{
    HRESULT hr;

    hr = CStunServer::CreateInstance(config, spServer.GetPointerPointer());
    if (FAILED(hr))
    {
        Logging::LogMsg(LL_ALWAYS, "Unable to initialize UDP server (error code = x%x)", hr);
        return hr;
    }

    hr = spServer->Start();
    if (FAILED(hr))
    {
        Logging::LogMsg(LL_ALWAYS, "Unable to start UDP server (error code = x%x)", hr);
        return hr;
    }

    return S_OK;
}

int main(){

    std::cout << "************* starting stuntman example ***************" << std::endl;

    typedef CRefCountedPtr<CStunServer> UdpServerPtr;

    CStunServerConfig config;

    config.addrPP = CSocketAddress(0, DEFAULT_STUN_PORT);
    config.fHasPP = true;

    UdpServerPtr udpServer;

    std::cout << "starting udp server " << std::endl;

    if(FAILED(StartUDP(udpServer, config))){
        std::cerr << "failed" << std::endl;
    }

    std::cout << "stopping udp server " << std::endl;

    udpServer->Stop();

    std::cout << "********************************************************" << std::endl;

    return 0;
}

#include <echomesh/util/EchomeshApplication.h>
#include <echomesh/util/Quit.h>

namespace echomesh {

namespace {

StringCaller CALLBACK;
void* USER_DATA;

CriticalSection LOCK;
bool STARTED = false;
const char* ARGV[] = {"cechomesh"};

string libraryName() { return ARGV[0]; }

class ApplicationBase : public juce::JUCEApplicationBase {
  public:
    virtual const String getApplicationName() { return libraryName(); }
    virtual const String getApplicationVersion() { return "0.0"; }
    virtual bool moreThanOneInstanceAllowed() { return false; }
    virtual void initialise(const String&) {
        if (CALLBACK and USER_DATA)
            CALLBACK(USER_DATA, "{\"event\":\"start\"}");
    }
    virtual void shutdown() {}
    virtual void anotherInstanceStarted(const String&) {}
    virtual void systemRequestedQuit() {
        ::echomesh::quit();
    }
    virtual void suspended() {}
    virtual void resumed() {}
    virtual void unhandledException(
        const std::exception*, const String& sourceFilename, int lineNumber) {
    }
};

juce::JUCEApplicationBase* juce_CreateApplication() {
    return new ApplicationBase();
}

}  // namespace

void callEchomesh(string const& s) {
    if (CALLBACK and USER_DATA)
        CALLBACK(USER_DATA, s.c_str());
}

void startApplication(StringCaller cb, void* userData) {
    {
        ScopedLock l(LOCK);
        STARTED = true;
    }

    CALLBACK = cb;
    USER_DATA = userData;
    juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
    juce::JUCEApplicationBase::main(1, ARGV);
}

bool isStarted() {
    ScopedLock l(LOCK);
    return STARTED;
}

}  // namespace echomesh
